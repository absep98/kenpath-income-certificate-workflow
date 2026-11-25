# Kenpath Assignment: Plan and Decisions

Deadline: **Thu 26 Nov 2026** (aim to submit evening of 25th). Budget: ~2 hrs/day, ~6 hrs total.
Mode: **teaching**. Claude explains each concept, Abhishek implements, Claude reviews.

## Assignment (summary)
Workflow app in a local language for government field/extension workers. Worker can:
1. See pending applications, most urgent first
2. Move each application through 3+ steps
3. Get AI help at each step where it genuinely helps
4. Approve / reject / return. Human always decides
5. See a clear history per application

Deliver by replying to the Kenpath email thread: GitHub repo link, live link + login credentials,
README (problem, workflow, where AI helps, impact measurement, technical decisions, run locally).
Optional: short video walkthrough.

## Decisions
- **Service:** Income Certificate (Karnataka, Nadakacheri-style). *Pending final confirmation.*
- **Language:** Kannada UI (strings kept in one file).
- **Idea:** a small **config-driven workflow engine**. A "service" is a config of steps, roles, checks.
  Income Certificate is the first service. A second one is optional if time allows. Portfolio story.
- **Stack (proposed):** FastAPI + SQLite/Postgres + React. Python for speed.
- **AI (kept small):**
  1. Verification: flag missing/inconsistent documents
  2. Review: summarise the case in plain Kannada for the Revenue Inspector
  3. Decision: draft a reason; officer edits and clicks the button
- **Concepts to learn:** state machine and transitions table, role-based access, append-only audit log,
  LLM structured output + human-in-the-loop, small evals, i18n.

## Day plan
- **Day 1 (23 Nov):** `docs/workflow.md`, then backend: DB, transitions, history log
- **Day 2:** Kannada frontend (list, detail, actions) + AI at each step
- **Day 3:** deploy (Render/Vercel), seed data, README, optional video

## Verified vs unverified
- Verified: the official Nadakacheri portal says RI (Revenue Inspector) and VA (Village Accountant)
  do field verification via the Samyojane mobile app (since 2019). Portal showed ~7,150 applications
  raised and ~6,640 disposed in Sep 2026.
- **Unverified (check before stating in README):** exact chain VA -> RI -> Tahsildar, fee (Rs 15 vs 25),
  timeline (7 vs 10-15 days). Blogs disagree. Ask someone who has applied, or check the portal.
- Kenpath's focus: not researched. Read their website before writing the README framing.

## Hosting
Render (backend) + Vercel or Render static (frontend). Test the live link in incognito.
Seed realistic demo data. Create a field-worker login and a supervisor login.

## Sources
- https://nadakacheri.karnataka.gov.in/ajsk
- https://www.indiafilings.com/learn/nadakacheri-income-caste-certificate-karnataka/
- https://testbook.com/articles/income-certificate-karnataka
