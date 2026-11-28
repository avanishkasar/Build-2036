# BUILD 2036: Win Research Dossier

Compiled 26 Nov 2026. Sources are listed at the end. Where something could not be verified, this file says so.

---

## 1. The hackathon: hard facts

| Item | Detail | Source |
|---|---|---|
| Organiser | Official hackathon of the **11th TiE Global Summit 2026** (host: TiE Indore). Hack2skill is the platform and innovation partner | tieglobalsummit.org/hackathon, hack2skill.com/event/build2036 |
| Team size | Hack2skill page says **Solo**. The FAQ says rules are "yet to be confirmed" | Hack2skill event page |
| Registration and submission | **19–30 Nov 2026** (closes Mon 30 Nov) | Both pages |
| What to submit | "Architecture, code repo, and working prototype demo link", plus an **impact case** | TiE page; Hack2skill FAQ #6 |
| Stage 1 screen | **1–2 Dec**: "Comprehensive technical & product screening conducted by Hack2skill" | TiE page |
| Stage 2 shortlist | **3–4 Dec**: TiE jury and steering committee pick the **Top 10** | TiE page |
| Announcement | 5 Dec: Top 10. 7 Dec: finalist induction and pitch mentoring | Both |
| Finale | **14 Dec** live demo day at Brilliant Convention Centre, Indore. **15 Dec** awards on the TGS100 "Recognize & Propel" main stage | Both |
| Prizes | **Overall, not per track.** ₹3,00,000 / ₹2,00,000 / ₹1,00,000. The six tracks compete against each other for three prizes | Hack2skill FAQ #8 |
| IP | Participants keep ownership | FAQ #11 |
| Extras | 2036 Capsule (recorded message), 2036 Wall showcase, investor access | Both |

**Implication:** because all six tracks share the same three prizes, the choice of track only matters for (a) how crowded it is and (b) how strongly it lands with the jury. There is no "safe track" with its own guaranteed winner.

### The six frontiers
1. Applied AI & Agentic Intelligence: multi-agent systems, vertical copilots, reasoning engines.
2. Climate & Clean Energy: grids, EV battery intelligence, water, decarbonisation.
3. **Digital Infrastructure**: sovereign cloud, DPI, **verifiable trust layers, high-scale payments, AI-resilient cybersecurity**.
4. Manufacturing Renaissance: smart factory, CV quality inspection, predictive maintenance.
5. Health, Longevity & Biotech: AI diagnostics, genomics, telemedicine.
6. The Rise of New India: Indore/MP, AgriTech, civic governance, **MSME digitisation**, skilling.

---

## 2. "Last 5 editions": the honest answer

**BUILD 2036 is a first edition.** No earlier BUILD hackathon exists, so there are no past BUILD winners to study. The closest predecessors and analogues are:

| # | Event | Link to BUILD 2036 | Winners and what won | What it tells us |
|---|---|---|---|---|
| 1 | **Rajasthan DigiFest × TiE Global Hackathon** (Dec 2025, VGU Jaipur) | Aligned to the **10th TGS**, the direct predecessor summit | 700+ participants, 250+ teams, 7 government-set themes. Winners: **UrbanFix** (digital agriculture), **Road ResQ** (health records + emergency response), **Rudra X** (smart road monitoring), **Accelar** (tourism footfall analytics), **Code Catalyst** (civic grievance), **Desert Innovators** (smart surveillance), **Spambots** (water governance) | Jury = government + industry + academia + TiE. Reported criteria: **"real deployment potential", scalability, feasibility, civic impact, alignment with public-sector needs**. Every winner is a concrete deployable public-system tool, not a toy |
| 2 | **TiE U Global Hackathon 2024** (Devpost) | TiE student hackathon | Business Innovation: **S.L.A.P.** (student–local-business digital mentorship, $2,000). Runners-up: BizElevate (AI mentorship for business owners), SentriBiz (**AI security advisor for small businesses**). Sustainability: Eco-scan (PPE recycling) | TiE rewards **business-model clarity and a named user** (local SMBs) as much as tech |
| 3 | **TiE Global Hackathon 2021** (first TiE hackathon) | TiE's first global hackathon | Team 7 (TiE Mumbai), WeHack (TiE Andhra Pradesh) | Too old to analyse in detail |
| 4 | **Google Cloud Gen AI Exchange 2025** (run by **Hack2skill**, the same screening partner) | Same evaluator org, same style of prototype screening | Overall: **PitchLense** (Team AIxpert): AI investment-analysis platform. Pro track: AI test-case generator for healthcare compliance. Student: **YouthMind** (mental wellness with a behavioural risk index). Others: CementAI (plant optimisation), ArtisanGully | Winners were **complete products**. PitchLense README: architecture diagram, process flow, 12+ features, deployed on Cloud Run, CI/CD, API docs, auth, browser extension, MCP server |
| 5 | **Solution Challenge 2026 India** (run by **Hack2skill**) | Same platform and evaluator rubric | **Asha AI** (MIT Aurangabad) won; Trouble Shooter (SPIT Mumbai), Function Override (DTU) | Published **Hack2skill rubric: Technical Merit 40% · Alignment with Cause 25% · Innovation 25% · UX 10%**. Technical Merit = complexity, **AI integration ("could a simpler approach have worked?")**, performance and scalability, **security and privacy** |

Gen AI Exchange's rubric (Hack2skill) also includes **Market Feasibility ~15%**. Edition-level weights could not be fully verified.

### What the judges are (two different audiences)

| Stage | Who | What they reward | Evidence |
|---|---|---|---|
| Screen (1–2 Dec) | **Hack2skill evaluators** | Rubric-driven: working prototype, architecture, code quality, real AI use, security, scalability | Solution Challenge 2026 published rubric |
| Shortlist + Finale | **TiE jury**: charter members, VCs. TGS100 juries have included Accel, Kalaari, Chiratae, Nu Ventures, SVQuad partners | **Innovation and IP, market validation, team capability, scalability, investment readiness, external validation (customers or experts)** | TGS100 criteria 2024/25 |

**Conclusion: the deck must win twice.** Pages 1–9 must satisfy a technical rubric (architecture, AI depth, security). Pages 10–14 must read like an investor pitch (market, model, moat, validation, why this founder).

---

## 3. How complete were winning projects?

From PitchLense (Gen AI Exchange 2025 overall winner, public repo) and the Solution Challenge requirements:
- **Live deployed URL** (Cloud Run), not localhost.
- Public **GitHub repo** with a README containing an architecture diagram, process flow, tech stack, quick-start, API endpoints and env-var docs.
- **3-minute demo video** (Hack2skill standard).
- **Deck** following the provided template: problem, solution, USP, features, process flow, architecture, wireframes or screens, tech stack, cost, future scope, links.
- Production signals: auth, CI/CD, security notes, an "extensions" surface (MCP server, browser extension).

**Bar to clear:** a deployed, end-to-end working path plus a repo that reads like a product. Ideas-only decks do not reach the finals of Hack2skill-screened events.

---

## 4. Deck and pitch tips from winners and judges (2025–2026)

1. **Read the rubric first and map every slide to a criterion.** (JetBrains judges, Jun 2026; AngelHack)
2. **One thing done extremely well beats five things half-done.** Scope to a single demo path. (JetBrains; AngelHack)
3. **Problem-first, never tool-first.** Open with a person and their pain, not your logo. (JetBrains; DEV 3-minute template)
4. **The demo is the centrepiece.** Something should be working within 90 s of the pitch. Pre-fill forms, mock slow calls, and keep a **backup recording**. (daily.dev summary of JetBrains; AngelHack demo tips)
5. **A 3-minute shape:** 0:00–0:20 hook, 0:20–0:40 solution in one line, 0:40–2:30 live demo, 2:30–3:00 impact, ask and roadmap. (Reskilll 2026; AngelHack 30/90/30/30)
6. **Judges decide in the first 30 seconds.** The title slide carries the one-line promise. (Reskilll)
7. **Points, diagrams and pictures, not paragraphs.** (SIH official pointers)
8. **Show originality explicitly.** Include a comparison against existing solutions; aim for at least 30% idea novelty, not just tech novelty. (SIH winners' guides)
9. **Investor juries need a market, a business model, validation and "why you".** (TGS100 criteria)
10. **Cite research and real data.** References slides are standard in SIH and Hack2skill-style templates and signal rigour.
11. **"Could a simpler approach have worked?"** This is a literal Hack2skill rubric question. Justify every AI component.

> Instagram reels could not be read from this environment because Instagram was blocked. Download any reels you want analysed and send them over.

---

## 5. Track (PS) selection

### Scoring the frontiers for *this* builder (backend + agents + security + Redis + K8s)

| Frontier | Crowding (est.) | Jury pull (TiE VCs) | Fit to builder | Prototype in 4 days | Verdict |
|---|---|---|---|---|---|
| 01 Applied AI & Agentic | **Very high**: every team builds an agent | Medium (agent fatigue) | High | High | Hard to stand out |
| 02 Climate | Medium | Medium | Low | Low (data, hardware) | No |
| **03 Digital Infrastructure** | **Low–medium** (hard track) | **High**: payments and trust are fundable infra | **Very high** (KAN-KubeAgent trust layer, FluxGuard) | High | **Pick** |
| 04 Manufacturing | Medium | Medium | Low | Low (CV data, hardware) | No |
| 05 Health | High | Medium | Low | Medium | No |
| 06 New India (Indore) | High (civic apps, like DigiFest winners) | High (home jury) | Medium | High | Fold in as the pilot story |

### The pick: Frontier 03 Digital Infrastructure, with 01 (agentic) and 06 (Indore MSME pilot) folded in

**Problem:** *AI agents are about to start paying on UPI, and there is no trust layer that verifies an agent, binds it to a user-signed mandate, stops it from being hijacked, and leaves evidence when something goes wrong.*

Why this wins:
- **Timely and unfilled.** NPCI is reported to be building a "Unified Agent Protocol" to register, verify and authorise agents on UPI with delegated spending limits. It was **not launched as of Nov 2026**. NPCI leadership said at GFF 2026 that agents may *recommend* payments but authentication and settlement must stay **deterministic and auditable**.
- **Proven threat.** A 2026 red-team study broke Google's AP2 agent-payment protocol with prompt injection ("Branded Whisper" and "Vault Whisper" attacks). A crypto agent moved $175k after treating a chatbot reply as an instruction.
- **Research-backed design.** Mandato (arXiv Aug 2026: signed mandates and a hash-chained audit proxy), Parallax (arXiv Apr 2026: cognitive–executive separation), Authenticated Delegation (ICML 2025: OAuth/OIDC agent delegation), and an access-control survey (arXiv Nov 2026).
- **Live market.** Pine Labs launched **P3P** (UPI agent payments on ReservePay/SBMD) in June 2026. Visa, Mastercard and Google AP2 are moving on cards. **India-scale, rail-agnostic, open enforcement plus evidence is still open.**
- **Scale.** UPI hit **25.47 bn transactions / ₹31.53 lakh crore in Oct 2026**. Udyam MSME registrations crossed **10 crore**. India agentic-AI market is projected at **~$5.3 bn by 2030** (MarketsandMarkets).
- **Jury resonance.** Fintech infrastructure is what TiE VCs fund. An **Indore MSME procurement pilot** gives the home jury its local story (Frontier 06).
- **Founder–problem fit.** You already built a symbolic trust layer for autonomous agents (KAN-KubeAgent) and a Redis sliding-window limiter (FluxGuard). That is exactly the "team capability" criterion.

Working name: **ADHIKAR** (अधिकार, "authority, right"). *Agents think. Adhikar decides.*

### Alternatives (if you want a different direction)
- **B. Udyog Agent (Frontier 06):** an Indore MSME compliance and credit copilot on Account Aggregator, GST and ONDC data. Stronger home-jury pull, but crowded and less technical differentiation.
- **C. AI-resilient DPI SOC (Frontier 03):** an agentic K8s security co-pilot for sovereign cloud, reusing KAN-KubeAgent. Fastest to build, but a weaker "2036 society impact" story for a VC jury.

---

## 6. Risks to state honestly

- The **prototype must exist by 30 Nov.** The screen is 40% technical merit, and the deck alone will not pass it.
- **Real UPI rails cannot be touched** without PSP access. The prototype uses a **simulated UPI ReservePay/OTM adapter**. The deck says so; judges respect honesty more than pretend integrations.
- Metric numbers in the deck are **design targets** until the red-team harness produces measured results. Replace them with real numbers before submitting.
- External validation (TGS100 criterion): get **2–3 real conversations** (an Indore MSME owner, a PSP or bank engineer) before 14 Dec and add their quotes.

---

## 7. Sources

- BUILD 2036, Hack2skill: https://hack2skill.com/event/build2036
- BUILD 2036, TiE Global Summit: https://tieglobalsummit.org/hackathon/
- Solution Challenge 2026 (Hack2skill rubric and winners): https://hack2skill.com/event/solution-challenge-2026
- Gen AI Exchange finale (Hack2skill blog): https://blog.hack2skill.com/gen-ai-exchange-hackathon-finale
- YourStory, Gen AI Exchange 10 innovations: https://yourstory.com/2025/12/google-cloud-gen-ai-exchange-hackathon-the-10-innovations-that-stood-out-this-year
- PitchLense repo: https://github.com/connectaman/PitchLense
- Rajasthan DigiFest × TiE winners (ANI / Business Standard): https://www.business-standard.com/content/press-releases-ani/rajasthan-digifest-x-tie-global-hackathon-announces-winners-showcases-national-scale-innovation-and-youth-participation-125121800011_1.html
- Inc42 on DigiFest × TiE: https://inc42.com/buzz/rajasthan-digifest-x-tie-global-hackathon-draws-700-participants-from-12-states/
- TiE U hackathon 2024 winners: https://houston.tie.org/programs/houston-students-win-top-prize-at-tie-u-global-hackathon/
- TGS100 criteria (2024): https://www.ciol.com/spotlight/tie-global-summit-2024-sets-100-cr-goal-50l-grants-to-top-3-winners-7370675
- JetBrains, notes from the judging table (Jun 2026): https://blog.jetbrains.com/ai/2026/06/how-to-win-a-hackathon-notes-from-the-judging-table/
- AngelHack, repeat winners: https://angelhack.com/blog/hackathon-tips-for-winners/
- Reskilll, 3-minute pitch: https://reskilll.com/blogs/hackathon-demo-presentation-tips-pitch-3-minutes-win-2026/
- NPCI at GFF 2026 (MediaNama): https://www.medianama.com/2026/09/223-npci-ai-agents-upi-payments/
- NPCI UAP (Business Standard): https://www.business-standard.com/finance/news/india-may-allow-agentic-ai-led-upi-transactions-under-new-npci-protocol-126070801343_1.html
- Pine Labs P3P: https://www.medianama.com/2026/06/223-pine-labs-agentic-payments-protocol-upi-liability-privacy-questions/
- UPI Oct 2026 record: https://www.medianama.com/2026/11/223-upi-p2m-p2p-transactions-october-2026/
- Udyam 10 crore: https://www.tribuneindia.com/news/credit-guarantee-scheme/msme-registrations-cross-10-crore-in-india-nearly-38-women-led-enterprises
- India agentic AI market: https://www.marketsandmarkets.com/Market-Reports/geography/agentic-ai-market/India
- arXiv 2601.22569, Red-teaming AP2: https://arxiv.org/abs/2601.22569
- arXiv 2604.12986, Parallax: https://arxiv.org/abs/2604.12986
- arXiv 2608.14074, Mandato: https://arxiv.org/abs/2608.14074
- arXiv 2501.09674, Authenticated Delegation: https://arxiv.org/abs/2501.09674
- arXiv 2611.06764, Access Control for AI Agents: https://arxiv.org/abs/2611.06764
- Deloitte agentic commerce estimate (via CTMfile): https://ctmfile.com
- Payment-agent risk report (via KuCoin): https://www.kucoin.com/news/flash/ai-payment-agents-face-limitations-and-security-risks-in-2026-report
