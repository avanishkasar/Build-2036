from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient  # noqa: E402

from adhikar.crypto import Signer  # noqa: E402
from adhikar.engine import Engine, verify_chain  # noqa: E402
from adhikar.models import Decision  # noqa: E402
from adhikar.scenario import AGENT, STEEL, intent, ramesh_mandate, rs, run_attacks, run_ramesh  # noqa: E402
from api.index import app  # noqa: E402


def test_ramesh_demo_outcomes() -> None:
    out = run_ramesh()
    assert [s["receipt"]["decision"] for s in out["steps"]] == ["ALLOW", "BLOCK", "ASK_PIN"]
    assert out["chain"]["valid"] is True


def test_every_attack_gets_expected_decision() -> None:
    out = run_attacks()
    failed = [c["attack"] for c in out["cases"] if not c["passed"]]
    assert not failed, failed


def test_tampered_receipt_breaks_chain() -> None:
    now = datetime.now(timezone.utc)
    eng = Engine(signer=Signer.generate(), registered_agents=frozenset({AGENT}))
    sm = ramesh_mandate(Signer.generate(), now)
    for _ in range(3):
        eng.decide(intent(now, payee=STEEL, amount=rs(1_000)), sm, now)
    assert verify_chain(eng.receipts, eng.signer.public_key_b64)[0]
    forged = list(eng.receipts)
    forged[1] = forged[1].model_copy(update={"decision": Decision.ALLOW, "amount": rs(99_000)})
    ok, msg = verify_chain(forged, eng.signer.public_key_b64)
    assert not ok and "Receipt 2" in msg
    assert not verify_chain([eng.receipts[0], eng.receipts[2]], eng.signer.public_key_b64)[0]


def test_monthly_cap_holds_across_payments() -> None:
    now = datetime.now(timezone.utc)
    eng = Engine(signer=Signer.generate(), registered_agents=frozenset({AGENT}))
    sm = ramesh_mandate(Signer.generate(), now)
    payees = [p.vpa for p in sm.mandate.payees]
    decisions = [eng.decide(intent(now, payee=payees[i % 6], amount=rs(45_000)), sm, now).decision for i in range(5)]
    assert decisions == [Decision.ALLOW] * 4 + [Decision.BLOCK]


def test_api_endpoints() -> None:
    c = TestClient(app)
    assert c.get("/api/health").json()["status"] == "ok"
    demo = c.post("/api/demo/ramesh").json()
    receipts = [s["receipt"] for s in demo["steps"]]
    assert c.post("/api/verify", json={"public_key": demo["adhikar_public_key"], "receipts": receipts}).json()["valid"]
    receipts[0]["amount"] = 1
    assert not c.post("/api/verify", json={"public_key": demo["adhikar_public_key"], "receipts": receipts}).json()["valid"]
    assert c.post("/api/demo/attacks").json()["passed"] == 11
