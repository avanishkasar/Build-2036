"""Ed25519 signing and canonical hashing."""

from __future__ import annotations

import base64
import hashlib
import json
import os
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from pydantic import BaseModel


def canonical(obj: BaseModel | dict[str, Any]) -> bytes:
    """Deterministic JSON bytes: sorted keys, no whitespace, ISO datetimes."""
    data = obj.model_dump(mode="json") if isinstance(obj, BaseModel) else obj
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def b64(data: bytes) -> str:
    return base64.b64encode(data).decode()


def unb64(data: str) -> bytes:
    return base64.b64decode(data, validate=True)


class Signer:
    def __init__(self, key: Ed25519PrivateKey) -> None:
        self._key = key
        self.public_key_b64 = b64(key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw))

    @classmethod
    def generate(cls) -> Signer:
        return cls(Ed25519PrivateKey.generate())

    @classmethod
    def from_env(cls, var: str = "ADHIKAR_SIGNING_SEED") -> Signer:
        """Load a 32 byte base64 seed from env, or generate an ephemeral key."""
        seed = os.environ.get(var)
        if seed:
            return cls(Ed25519PrivateKey.from_private_bytes(unb64(seed)))
        return cls.generate()

    def sign(self, payload: bytes) -> str:
        return b64(self._key.sign(payload))


def verify(public_key_b64: str, payload: bytes, signature_b64: str) -> bool:
    try:
        Ed25519PublicKey.from_public_bytes(unb64(public_key_b64)).verify(unb64(signature_b64), payload)
        return True
    except (InvalidSignature, ValueError):
        return False
