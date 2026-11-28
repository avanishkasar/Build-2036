"""The deterministic policy core. No model is called anywhere in this file.

Every intent runs through the same checks. Any failed BLOCK check blocks. Otherwise any
failed ASK_PIN check asks the user. Otherwise the payment is allowed. Every decision is
written as a signed receipt chained to the previous one.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

from .crypto import Signer, canonical, sha256_hex, verify
from .models import Check, Decision, Origin, PaymentIntent, Receipt, SignedMandate
from .store import InMemoryStore

GENESIS = "0" * 64
MAX_INTENT_AGE = timedelta(minutes=5)
MAX_CLOCK_SKEW = timedelta(seconds=30)
TRUSTED_ORIGINS = frozenset({Origin.USER, Origin.MANDATE, Origin.TRUSTED_TOOL})


def _rupees(paise: int) -> str:
    """Indian digit grouping: Rs 1,84,000."""
    rupees, rem = divmod(paise, 100)
    s = str(rupees)
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        groups = []
        while len(head) > 2:
            groups.insert(0, head[-2:])
            head = head[:-2]
        if head:
            groups.insert(0, head)
        s = ",".join(groups) + "," + tail
    return f"Rs {s}" + (f".{rem:02d}" if rem else "")


@dataclass
class Engine:
    signer: Signer
    registered_agents: frozenset[str]
    store: InMemoryStore = field(default_factory=InMemoryStore)
    receipts: list[Receipt] = field(default_factory=list)

    def decide(self, intent: PaymentIntent, signed: SignedMandate, now: datetime | None = None) -> Receipt:
        started = time.perf_counter_ns()
        now = now or datetime.now(timezone.utc)
        m = signed.mandate
        checks: list[Check] = []

        def add(code: str, passed: bool, severity: Decision, detail: str) -> None:
            checks.append(Check(code=code, passed=passed, severity=severity, detail=detail))

        with self.store.lock:
            # 1. Mandate is genuine and is the one the intent refers to.
            sig_ok = verify(signed.user_public_key, canonical(m), signed.signature)
            add("MANDATE_SIGNATURE", sig_ok, Decision.BLOCK, "User signature on mandate verified" if sig_ok else "Mandate signature invalid or tampered")
            match = intent.mandate_id == m.mandate_id
            add("MANDATE_MATCH", match, Decision.BLOCK, "Intent references this mandate" if match else "Intent references a different mandate")

            # 2. Agent identity.
            known = intent.agent_id in self.registered_agents
            bound = intent.agent_id in m.agent_ids
            add("AGENT_REGISTERED", known, Decision.BLOCK, f"Agent {intent.agent_id} is registered" if known else f"Unknown agent {intent.agent_id}")
            add("AGENT_IN_MANDATE", bound, Decision.BLOCK, "Agent is named in the mandate" if bound else "Agent is not named in the mandate")

            # 3. Freshness and replay.
            active = m.valid_from <= now <= m.valid_until
            add("MANDATE_ACTIVE", active, Decision.BLOCK, "Mandate is within its validity window" if active else "Mandate expired or not yet active")
            age = now - intent.issued_at
            fresh = -MAX_CLOCK_SKEW <= age <= MAX_INTENT_AGE
            add("INTENT_FRESH", fresh, Decision.BLOCK, "Intent issued within the last 5 minutes" if fresh else "Intent is stale or from the future")
            replay = self.store.nonce_seen(intent.nonce, now)
            add("NOT_REPLAYED", not replay, Decision.BLOCK, "Nonce never seen before" if not replay else "Nonce already used: replayed request")

            # 4. Mandate scope.
            allowed_payees = {p.vpa.lower(): p.name for p in m.payees}
            payee_ok = intent.payee_vpa.lower() in allowed_payees
            add("PAYEE_IN_MANDATE", payee_ok, Decision.BLOCK, f"Payee is approved: {allowed_payees.get(intent.payee_vpa.lower())}" if payee_ok else f"Payee {intent.payee_vpa} is not in the mandate")
            purpose_ok = intent.purpose in m.purposes
            add("PURPOSE_IN_MANDATE", purpose_ok, Decision.BLOCK, f"Purpose '{intent.purpose}' is allowed" if purpose_ok else f"Purpose '{intent.purpose}' is not allowed")

            # 5. Provenance: payee and amount must not come from untrusted content.
            payee_clean = intent.payee_origin in TRUSTED_ORIGINS
            add("PAYEE_PROVENANCE", payee_clean, Decision.BLOCK, "Payee came from a trusted source" if payee_clean else "Payee was taken from untrusted web content")
            amount_clean = intent.amount_origin in TRUSTED_ORIGINS
            add("AMOUNT_PROVENANCE", amount_clean, Decision.BLOCK, "Amount came from a trusted source" if amount_clean else "Amount was taken from untrusted web content")

            # 6. Limits.
            under_txn = 0 < intent.amount <= m.per_txn_cap
            add("PER_TXN_CAP", under_txn, Decision.BLOCK, f"{_rupees(intent.amount)} within per payment cap {_rupees(m.per_txn_cap)}" if under_txn else f"{_rupees(intent.amount)} exceeds per payment cap {_rupees(m.per_txn_cap)}")
            spent = self.store.month_spend(m.mandate_id, now)
            under_month = spent + intent.amount <= m.monthly_cap
            add("MONTHLY_CAP", under_month, Decision.BLOCK, f"Month total {_rupees(spent + intent.amount)} within {_rupees(m.monthly_cap)}" if under_month else f"Month total would reach {_rupees(spent + intent.amount)}, cap is {_rupees(m.monthly_cap)}")
            recent = self.store.recent(m.mandate_id, intent.payee_vpa.lower(), now, m.window_seconds)
            window_sum = sum(a for _, a in recent) + intent.amount
            split_ok = window_sum <= m.per_txn_cap or len(recent) == 0
            add("SPLIT_PAYMENTS", split_ok, Decision.BLOCK, "No payment splitting detected" if split_ok else f"{len(recent) + 1} payments to one payee in {m.window_seconds // 60} min sum to {_rupees(window_sum)}, above the per payment cap")
            velocity_ok = len(recent) < m.max_txn_per_payee_window
            add("VELOCITY", velocity_ok, Decision.ASK_PIN, "Normal payment frequency" if velocity_ok else f"{len(recent) + 1} payments to one payee within {m.window_seconds // 60} min")
            small = intent.amount <= m.pin_above
            add("PIN_THRESHOLD", small, Decision.ASK_PIN, f"Below the {_rupees(m.pin_above)} approval threshold" if small else f"Above {_rupees(m.pin_above)}: user must approve with UPI PIN")

            failed = [c for c in checks if not c.passed]
            if any(c.severity is Decision.BLOCK for c in failed):
                decision = Decision.BLOCK
            elif failed:
                decision = Decision.ASK_PIN
            else:
                decision = Decision.ALLOW

            # Commit state. Nonces are burned even on BLOCK so a blocked request can't be retried as is.
            self.store.remember_nonce(intent.nonce, now)
            if decision is Decision.ALLOW:
                self.store.add_spend(m.mandate_id, now, intent.amount)
                self.store.add_recent(m.mandate_id, intent.payee_vpa.lower(), now, intent.amount)

            latency_us = (time.perf_counter_ns() - started) // 1000
            receipt = Receipt(
                seq=len(self.receipts) + 1,
                prev_hash=self.receipts[-1].receipt_hash if self.receipts else GENESIS,
                intent_hash=sha256_hex(canonical(intent)),
                intent_id=intent.intent_id,
                mandate_id=m.mandate_id,
                agent_id=intent.agent_id,
                payee_vpa=intent.payee_vpa,
                amount=intent.amount,
                decision=decision,
                reasons=[c.detail for c in failed] or ["All checks passed"],
                checks=checks,
                decided_at=now,
                latency_us=latency_us,
            )
            body = canonical(receipt.model_dump(mode="json", exclude={"receipt_hash", "signature"}))
            receipt = receipt.model_copy(update={"receipt_hash": sha256_hex(body), "signature": self.signer.sign(body)})
            self.receipts.append(receipt)
            return receipt


def verify_chain(receipts: list[Receipt], public_key_b64: str) -> tuple[bool, str]:
    """Recompute every hash and signature. Any edit, reorder or deletion is detected."""
    prev = GENESIS
    for i, r in enumerate(receipts, start=1):
        if r.seq != i:
            return False, f"Receipt {i}: sequence number is {r.seq}"
        if r.prev_hash != prev:
            return False, f"Receipt {i}: chain broken, previous hash does not match"
        body = canonical(r.model_dump(mode="json", exclude={"receipt_hash", "signature"}))
        if sha256_hex(body) != r.receipt_hash:
            return False, f"Receipt {i}: contents were modified"
        if not verify(public_key_b64, body, r.signature):
            return False, f"Receipt {i}: signature invalid"
        prev = r.receipt_hash
    return True, f"All {len(receipts)} receipts verified"
