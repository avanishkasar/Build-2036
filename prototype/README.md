# Adhikar prototype

Agents think. Adhikar decides. A deterministic trust layer between AI agents and UPI.

**Live demo:** see the deployment link in the main README. Add `?judge` to the URL to run the demo on load.

## What it does

An agent proposes a payment. The policy engine (`adhikar/engine.py`) checks it against a mandate the user signed once with Ed25519. No model is called anywhere in the decision path. Every request ends as `ALLOW`, `ASK_PIN` or `BLOCK`, and every decision is written as an Ed25519 signed receipt, hash chained to the one before it.

Checks, in order: mandate signature, mandate match, agent registered, agent named in mandate, mandate active, intent fresh (5 min), nonce not replayed, payee in mandate, purpose in mandate, payee provenance, amount provenance, per payment cap, monthly cap, split payments, velocity, PIN threshold.

## Measured results

Run `python -m pytest -q tests` or press "Run the attack suite" on the live page. 11 designed attack cases (prompt injection, payee swap with a lookalike UPI ID, amount inflation, replay, split payments, expired mandate, unknown agent, tampered mandate, stale request, wrong purpose, plus a legitimate control) all return the expected decision. Decision latency on the dev container over 2,000 runs: p50 0.23 ms, p95 0.40 ms, in process, without network.

## Honest limits of this prototype

- The agent is scripted. Adhikar does not trust the agent, so the checks are identical for LangGraph or any other framework, but no LLM runs in this demo.
- The UPI rail is not connected. No real money moves.
- State is in memory per request. The production path is Redis for nonces and sliding windows and PostgreSQL for the receipt ledger.
- The split payment rule can flag two legitimate orders to one supplier within 15 minutes if together they exceed the per payment cap.

## Run locally

```bash
pip install -r requirements.txt uvicorn pytest httpx
```

```bash
python -m pytest -q tests
```

```bash
uvicorn api.index:app --reload
```
