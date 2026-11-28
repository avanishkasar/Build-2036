"""HTTP API for the Adhikar prototype (Vercel Python function)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI, HTTPException  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from pydantic import BaseModel, Field  # noqa: E402

from adhikar import __version__  # noqa: E402
from adhikar.engine import verify_chain  # noqa: E402
from adhikar.models import Receipt  # noqa: E402
from adhikar.scenario import run_attacks, run_ramesh  # noqa: E402

app = FastAPI(title="Adhikar API", version=__version__, docs_url="/api/docs", openapi_url="/api/openapi.json")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET", "POST"], allow_headers=["content-type"])


class VerifyRequest(BaseModel):
    public_key: str = Field(min_length=40, max_length=64)
    receipts: list[Receipt] = Field(min_length=1, max_length=500)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "version": __version__}


@app.post("/api/demo/ramesh")
def demo_ramesh() -> dict:
    return run_ramesh()


@app.post("/api/demo/attacks")
def demo_attacks() -> dict:
    return run_attacks()


@app.post("/api/verify")
def verify_receipts(req: VerifyRequest) -> dict:
    try:
        ok, msg = verify_chain(req.receipts, req.public_key)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"valid": ok, "message": msg}
