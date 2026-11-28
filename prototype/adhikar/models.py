"""Typed domain models for the Adhikar policy core.

All money is held as integer paise to avoid float rounding on payment amounts.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator

Paise = Annotated[int, Field(ge=0, le=10_000_000_000)]  # up to Rs 10 crore
Vpa = Annotated[str, Field(min_length=3, max_length=255, pattern=r"^[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}$")]


class Origin(str, Enum):
    """Where a field in a payment intent came from."""

    USER = "user"
    MANDATE = "mandate"
    TRUSTED_TOOL = "trusted_tool"
    UNTRUSTED_WEB = "untrusted_web"


class Decision(str, Enum):
    ALLOW = "ALLOW"
    ASK_PIN = "ASK_PIN"
    BLOCK = "BLOCK"


class Payee(BaseModel):
    model_config = ConfigDict(frozen=True)

    vpa: Vpa
    name: str = Field(min_length=1, max_length=120)


class Mandate(BaseModel):
    """What the user allows an agent to pay for. Signed once by the user."""

    model_config = ConfigDict(frozen=True)

    mandate_id: str = Field(min_length=4, max_length=64)
    user_id: str = Field(min_length=1, max_length=64)
    agent_ids: tuple[str, ...] = Field(min_length=1)
    payees: tuple[Payee, ...] = Field(min_length=1)
    purposes: tuple[str, ...] = Field(min_length=1)
    per_txn_cap: Paise
    monthly_cap: Paise
    pin_above: Paise
    max_txn_per_payee_window: int = Field(default=3, ge=1, le=100)
    window_seconds: int = Field(default=900, ge=60, le=86_400)
    valid_from: datetime
    valid_until: datetime

    @field_validator("valid_until")
    @classmethod
    def _until_after_from(cls, v: datetime, info) -> datetime:  # type: ignore[no-untyped-def]
        start = info.data.get("valid_from")
        if start is not None and v <= start:
            raise ValueError("valid_until must be after valid_from")
        return v


class SignedMandate(BaseModel):
    model_config = ConfigDict(frozen=True)

    mandate: Mandate
    user_public_key: str  # base64 raw Ed25519 public key
    signature: str  # base64 Ed25519 signature over canonical JSON of mandate


class PaymentIntent(BaseModel):
    """What the agent proposes. The agent is never trusted; provenance is recorded by the gateway."""

    model_config = ConfigDict(frozen=True)

    intent_id: str = Field(min_length=4, max_length=64)
    agent_id: str = Field(min_length=1, max_length=64)
    mandate_id: str
    payee_vpa: Vpa
    amount: Paise
    purpose: str = Field(min_length=1, max_length=64)
    nonce: str = Field(min_length=8, max_length=128)
    issued_at: datetime
    payee_origin: Origin
    amount_origin: Origin
    note: str = Field(default="", max_length=280)


class Check(BaseModel):
    code: str
    passed: bool
    severity: Decision  # outcome this check forces when it fails
    detail: str


class Receipt(BaseModel):
    seq: int
    prev_hash: str
    intent_hash: str
    intent_id: str
    mandate_id: str
    agent_id: str
    payee_vpa: str
    amount: int
    decision: Decision
    reasons: list[str]
    checks: list[Check]
    decided_at: datetime
    latency_us: int
    receipt_hash: str = ""
    signature: str = ""
