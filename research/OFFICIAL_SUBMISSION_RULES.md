# BUILD 2036: Official Submission Rules

Compiled 26 Nov 2026. Submission closes Mon 30 Nov 2026.

## Read this first: what is confirmed and what is not

The Hack2skill dashboard (https://hack2skill.com/event/build2036/dashboard/roadmap) needs a login. This pass ran in a cloud container with no access to your logged in Chrome, so I could not open the dashboard, the submission form or the official PPT template. The Hack2skill API and X were also blocked from here.

Everything below is labelled:

- **Confirmed**: read directly on a public official page.
- **Likely**: the standard Hack2skill pattern from their other events. Treat it as a strong guess and check it against the dashboard.
- **Unknown**: only the logged in dashboard can answer.

**Before 30 Nov, open the dashboard yourself and fill the gaps in section 4.** It takes about 10 minutes.

---

## 1. Confirmed from official public pages

Source: TiE Global Summit hackathon page, https://tieglobalsummit.org/hackathon/ (fetched 26 Nov 2026).

| Item | Official wording |
|---|---|
| What to submit | "Submit architecture, code repo, and working prototype demo link." |
| Stage 3 description | "Submit your prototype, architecture, and impact case for expert evaluation. Ten finalist teams are selected to advance to the live in person Finale at TGS 2026." |
| Submission window | 19 to 30 November 2026 |
| Stage 1 screening | 1 to 2 Dec: "Comprehensive technical & product screening conducted by Hack2skill." |
| Stage 2 shortlist | 3 to 4 Dec: "TiE jury and steering committee review to select Top 10 finalists." |
| Top 10 announced | 5 Dec |
| Finalist induction | 7 Dec: "Virtual briefing, logistics orientation, and pitch mentoring for finalists." |
| Live demo day | 14 Dec, Brilliant Convention Centre, Indore: "Finalist teams pitch live before the grand jury." |
| Awards | 15 Dec, TGS Main Stage, TGS100 "Recognize & Propel" segment |
| Prizes | INR 3,00,000 / 2,00,000 / 1,00,000. Overall, not per track |
| Mentoring | "Structured mentoring sessions with TiE charter members and technology architects." No names published |
| What they want | "Bring a meaningful problem, a working AI prototype, and the ambition to pitch before global TiE founders and investors in Indore." |
| IP | "Participants retain ownership of the solutions they build." |
| Rules caveat | "Participation, eligibility, judging, and event access are subject to the published BUILD 2036 programme rules." |

**So the four things to submit are: architecture, code repo, working prototype demo link, and an impact case.** The impact case is easy to miss. It is the only one that is not a link.

## 2. Likely, from the Hack2skill pattern on other events

Hack2skill runs Solution Challenge 2026 and Gen AI Exchange, and every recent event has used the same submission shape. Sources: Solution Challenge 2026 event page (https://hack2skill.com/event/solution-challenge-2026), GDG Solution Challenge 2025 info deck on SlideShare (https://www.slideshare.net/slideshow/gdg-solutions-challenge-with-hack2skill-pptx/275327339), Hack2skill AI for Good page (https://hack2skill.com/event/ai-for-good).

| Item | Hack2skill pattern | Confidence |
|---|---|---|
| Deck | Their own PPT template, downloaded from the submission dashboard. The template is not public | High |
| Deck format | Upload as PDF | Medium |
| Demo video | Public YouTube or Vimeo (unlisted is usually fine), **3 minutes maximum** | High |
| GitHub | Public repo link | High |
| Live prototype | Working URL that judges can open | High |
| Language | English | High |
| Rubric (screening) | Technical Merit 40%, Alignment with cause 25%, Innovation 25%, UX 10%. Published for Solution Challenge 2026. Not confirmed for BUILD 2036 | Medium |
| Gen AI Exchange jury criteria | Technical innovation, feasibility of implementation, clarity of impact, potential to scale beyond the prototype (YourStory, Dec 2025) | Reported |

### The Hack2skill prototype template slide order

This is the order your Canva deck already follows. It matches the Gen AI Exchange and Solution Challenge prototype templates as recalled from past events. I could not download the BUILD 2036 copy to confirm it.

1. Title: team name, team leader, problem statement or track
2. Brief about the solution
3. Opportunities: how is it different, how does it solve the problem, USP
4. List of features
5. Process flow or use case diagram
6. Wireframes or mockups of the prototype
7. Architecture diagram
8. Technologies used
9. Estimated implementation cost
10. Snapshots of the prototype
11. Prototype performance report or benchmarks
12. Additional details and future development
13. Links: GitHub, demo video (3 min), live prototype URL

**Two slides in this list are missing from the current deck: "Snapshots of the prototype" and "Links".** Both need real assets, so I left a comment in Canva rather than inventing them.

## 3. What a BUILD 2036 competitor is already submitting

Two other BUILD 2036 entrants have public repos. Both show what "complete" looks like for this event.

**Saakh** (https://github.com/KomalSrinivasan/saakh), KCC loan appraisal for cooperative bank officers:
- Header line: Live app, Demo video, Architecture, Impact case, "Built for BUILD 2036 (TiE Global Summit 2026 x Hack2skill)". These are exactly the four official deliverables.
- Live app has a `?judge` URL that skips sign in and opens a demo mode with sample data.
- 1:41 demo video recorded on a real phone against the live site, plus a 24 second teaser and a GIF preview in the README.
- 12 screenshots in tables, a "Try it in two minutes" section, a "Testing status" section and a "Data honesty" section.
- A separate `docs/impact-case.md` with problem, who benefits, how it solves it, a sourced figures table, and an explicit list of what they have not measured.
- **Same design rule as ADHIKAR**: "AI handles words. The engine handles numbers. The officer decides." A deterministic rules engine plus a verification harness on the agent. Expect judges to see both and compare them.

**Agentic Revenue Assurance Copilot** (https://github.com/priyamsinghjhs/build2036-revenue-assurance-agent): Frontier 01, multi agent LangGraph system with a live Cloudflare URL and a "Why this fits BUILD 2036" section.

**What this means for ADHIKAR:** the bar is a live URL with a judge mode, a short real demo video, screenshots, an impact case document and honest testing notes. The "deterministic code decides" idea is no longer unique on its own. ADHIKAR's edge has to come from the payments threat model (prompt injection, payee swap, replay), signed mandates and receipts, and the UPI and NPCI timing.

## 4. Fill these in from the dashboard before submitting

- [ ] Download the official PPT template and diff its slide list against section 2
- [ ] Exact demo video limit (expected 3 minutes)
- [ ] File format and size limit for the deck (PDF expected)
- [ ] Is the impact case a separate upload, a text field or a deck slide?
- [ ] Is the architecture a separate upload or part of the deck?
- [ ] Team size rule (the event page said Solo, the FAQ said not final)
- [ ] Track and problem statement field: pick Frontier 03 Digital Infrastructure
- [ ] Any published judging criteria or weights for BUILD 2036 itself
- [ ] Whether a submission can be edited after it is sent

## 5. Judges and mentors

No BUILD 2036 jury, mentor list or announcement naming people could be found in public search results as of 26 Nov 2026. TiE Indore's site (https://indore.tie.org/tgs2026/) blocked automated access, and LinkedIn and X results were not reachable from this environment. The only official line is that mentoring comes from "TiE charter members and technology architects".

The TGS100 juries in earlier editions included partners from Accel, Kalaari, Chiratae, Nu Ventures and SVQuad (see BUILD2036_RESEARCH.md). Treat that as a guide to who the Stage 2 jury might be, not a confirmed list. Check the TiE Indore and Hack2skill LinkedIn pages from your own browser after 5 Dec for the finalist briefing.

## Sources

- TiE Global Summit hackathon page: https://tieglobalsummit.org/hackathon/
- Hack2skill event page: https://hack2skill.com/event/build2036
- Hack2skill launch post on X: https://x.com/hack2skill/status/2124065278719832150 (not readable from here)
- Solution Challenge 2026: https://hack2skill.com/event/solution-challenge-2026
- GDG Solution Challenge 2025 info deck: https://www.slideshare.net/slideshow/gdg-solutions-challenge-with-hack2skill-pptx/275327339
- Hack2skill AI for Good: https://hack2skill.com/event/ai-for-good
- Gen AI Exchange winners (YourStory): https://yourstory.com/2025/12/google-cloud-gen-ai-exchange-hackathon-the-10-innovations-that-stood-out-this-year
- Saakh repo: https://github.com/KomalSrinivasan/saakh
- Revenue Assurance Copilot repo: https://github.com/priyamsinghjhs/build2036-revenue-assurance-agent
