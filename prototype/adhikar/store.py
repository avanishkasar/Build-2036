"""State the policy engine needs: seen nonces, monthly spend, recent payments per payee.

The in memory store is process local and guarded by a lock so check and commit are atomic.
A Redis backed store with the same interface is the production path (FluxGuard style
sliding windows); it is not wired into this prototype.
"""

from __future__ import annotations

import threading
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class InMemoryStore:
    nonce_ttl_seconds: int = 86_400
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)
    _nonces: dict[str, datetime] = field(default_factory=dict)
    _spend: dict[tuple[str, str], int] = field(default_factory=lambda: defaultdict(int))
    _recent: dict[tuple[str, str], deque[tuple[datetime, int]]] = field(default_factory=lambda: defaultdict(deque))

    @property
    def lock(self) -> threading.Lock:
        return self._lock

    # All methods below assume the caller holds self.lock.

    def nonce_seen(self, nonce: str, now: datetime) -> bool:
        self._expire_nonces(now)
        return nonce in self._nonces

    def remember_nonce(self, nonce: str, now: datetime) -> None:
        self._nonces[nonce] = now

    def month_spend(self, mandate_id: str, now: datetime) -> int:
        return self._spend[(mandate_id, now.strftime("%Y-%m"))]

    def add_spend(self, mandate_id: str, now: datetime, amount: int) -> None:
        self._spend[(mandate_id, now.strftime("%Y-%m"))] += amount

    def recent(self, mandate_id: str, payee: str, now: datetime, window_seconds: int) -> list[tuple[datetime, int]]:
        q = self._recent[(mandate_id, payee)]
        while q and (now - q[0][0]).total_seconds() > window_seconds:
            q.popleft()
        return list(q)

    def add_recent(self, mandate_id: str, payee: str, now: datetime, amount: int) -> None:
        self._recent[(mandate_id, payee)].append((now, amount))

    def _expire_nonces(self, now: datetime) -> None:
        if len(self._nonces) < 10_000:
            return
        cutoff = [n for n, t in self._nonces.items() if (now - t).total_seconds() > self.nonce_ttl_seconds]
        for n in cutoff:
            del self._nonces[n]
