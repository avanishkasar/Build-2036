# Hack2skill submission form: ADHIKAR

Copy each block into the matching field. Character counts are checked against the 1024 limit.

## Challenges

Frontier 03: Digital Infrastructure

## Prototype Brief

AI agents will soon pay on UPI, and one hidden line on a web page can trick an agent into paying a scammer. Adhikar is a trust layer between any AI agent and UPI. The agent proposes a payment; plain code, not the model, checks it against a mandate the user signed once with Ed25519: approved payees, purpose, per payment and monthly caps, a UPI PIN threshold and a validity window. Every request ends as Allowed, Ask for UPI PIN, or Blocked, with a signed receipt hash chained to the last, so any edit is caught. Our live prototype runs 16 checks per payment, including payee and amount provenance to stop prompt injection. In its attack suite, 11 of 11 cases return the expected decision, covering injection, lookalike UPI IDs, inflated amounts, replay, split payments and tampered mandates, in under half a millisecond per decision. Demo: an Indore MSME procurement agent, with UPI in sandbox.

## What is the tech stack being used in your solution?

Prototype (live): Python 3.13, FastAPI and Pydantic v2 for the policy gateway and API; cryptography library for Ed25519 signed mandates and signed, SHA-256 hash chained decision receipts; a deterministic rules engine with no model in the decision path; pytest attack suite; a static web UI built with Tailwind CSS and self hosted fonts; deployed on Vercel serverless functions. State (nonces, monthly spend, sliding windows) is in memory per run in the prototype.
Production path: Redis sliding window velocity and replay checks (reusing our FluxGuard limiter), PostgreSQL evidence ledger, FastAPI on Kubernetes, a LangGraph procurement agent with Gemini that only proposes intents, MCP client support, and adapters for UPI ReservePay and One Time Mandate once a payment provider sandbox is available.

## GitHub Public Repository Link

https://github.com/avanishkasar/Build-2036

(The prototype lives in the `prototype/` folder. Merge the open pull request into `main` before submitting so judges see it on the default branch.)

## Demo Video Link

Paste your YouTube link after uploading `ADHIKAR_demo.mp4` (set visibility to Unlisted or Public).

## Deployed Link (If any)

https://adhikar-sigma.vercel.app/?judge

## Upload your Solution Deck/PPT

Upload the updated deck as PDF after the fixes listed in the chat (real screenshots on slide 11, measured results on slide 12, links on slide 13, prototype vs production stack on slides 7 and 8).
