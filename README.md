# Income Certificate Workflow (Kannada)

A workflow app that helps Karnataka revenue officers move Income Certificate applications from intake to a final decision, in Kannada, with AI help at each step and a human making every decision.

**Live app:** https://kenpath-workflow.onrender.com (free hosting: the first load after idle can take about 50 seconds)
**Demo logins** (password for all: `demo123`): `suresh` (Village Accountant), `meena` (Revenue Inspector), `rao` (Tahsildar)

## 1. The problem and who it affects

Citizens need an income certificate for scholarships, fee waivers and welfare schemes. In Karnataka the application passes through village-level and taluk-level officers (Nadakacheri / Atalji Janasnehi Kendra is the citizen-facing counter). Each officer works through a pile of cases and has to work out which ones are stuck, which are missing documents, and which look suspicious. Applicants wait, and officers lose time on cases that were never complete.

Who it affects: rural applicants waiting on a certificate, and the field and revenue officers who process them, many of whom work on a phone and read Kannada first.

## 2. What the app does

Each officer logs in and sees only the cases waiting for their role, **oldest and most urgent first** (colour-coded by days waiting). They open a case, see the facts, a document checklist and an AI panel, and then forward, return or reject it. Every action is written to a per-case history.

Workflow (4 stages, each with its own officer):

| Stage | Who acts | Can do |
|---|---|---|
| Submitted / intake | Village Accountant | forward, reject |
| Field verification | Village Accountant | forward, return, reject |
| Revenue Inspector review | Revenue Inspector | forward, return to field verification, reject |
| Final decision | Tahsildar | approve, reject, return to RI |

Approved and Rejected are final. Return and reject require a written reason.

The UI is Kannada by default with an English toggle, and is built mobile-first with large tap targets.

**Caveat on the process itself:** the officer chain above (Village Accountant, Revenue Inspector, Tahsildar) is based on public sources about Karnataka's Nadakacheri process. I did not verify the exact fee, timeline or which officer holds final authority in every district. Treat the stages as a reasonable model, not an official specification. See `docs/workflow.md`.

## 3. Where AI helps, and why

AI only suggests. It never moves a case. The approve, reject and return buttons are always the officer's.

Two layers:

1. **Rule checks (plain Python, always on).** Flags missing documents and unusually high declared income. These are deterministic, instant, explainable and free, so they should not depend on an LLM.
2. **LLM assistance (Groq, `openai/gpt-oss-120b`).** Writes a short Kannada (or English) summary of the case and drafts a decision note the officer can use or edit. This is what an officer would otherwise write by hand for every case.

If the LLM is down, rate-limited or has no key, the rule flags still appear and the app keeps working. The LLM only sees the case facts and is told not to invent anything.

Limits I know about: the income ceiling (₹3,00,000) is an illustrative demo threshold, not an official one. LLM Kannada is good for short plain sentences but can be stilted. The free tier has rate limits.

## 4. How to measure impact, and why it should work

Measure against a baseline taken before rollout:

- **Time per case** at each stage (history already stores timestamps for every step).
- **Return rate**: the share of cases sent back for missing documents. The rule flags should lower this over time because gaps are caught at intake.
- **Age of the oldest pending case** per officer. The urgency-ordered queue targets this directly.
- **Officer override rate** on AI suggestions. If officers rarely edit the drafted reason, it is useful. If they always rewrite it, it is not.

Why it should work: the delays come from cases sitting unnoticed and from incomplete files reaching later stages. The queue surfaces what needs attention first, and the checks catch gaps at the earliest stage. This is a prototype and I have no real usage data; these are the measurements I would collect in a pilot, not results I have.

## 5. Main technical decisions

- **Workflow as a state machine.** One `TRANSITIONS` table maps (state, action, role) to the next state. Every rule lives in one place and is unit-tested, including that final states are dead ends and that the wrong role is rejected.
- **Append-only audit history.** Every action writes a history row in the same database transaction as the status change, so status and history can never disagree. A failed action rolls back both (tested).
- **Roles are enforced on the server.** The JWT only identifies the user. The role is looked up server-side, so a client cannot claim a different role. Wrong-role actions return 403.
- **No frontend build step.** Plain HTML, CSS and JavaScript served by FastAPI. One deployable service, nothing to compile, and quick to load on weak connections.
- **SQLite.** Enough for a demo. The demo DB is re-seeded on start when empty because free hosting has an ephemeral disk. For production I would use Postgres with Alembic migrations (`create_all` does not alter existing tables).
- **AI as an optional layer.** Isolated in `backend/ai.py` so its failure cannot affect the workflow.

Known shortcuts (honest list): demo passwords are plain text in code; the "reason required for return/reject" rule is enforced in the UI but not yet on the server; there is no citizen-facing intake form (cases are seeded); API tests are limited to the workflow and service layers.

## 6. Run locally

Requires Python 3.12+.

```powershell
cd backend
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe seed.py        # optional: loads 8 demo cases
.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Open http://localhost:8000. To enable the LLM part, put `GROQ_API_KEY=your_key` in a `.env` file in `backend/` (never commit it). Without a key the app still runs with rule flags only.

Run the tests: `.venv\Scripts\python.exe -m pytest -q` (14 tests).

## Layout

```
backend/
  workflow.py   state machine and transition rules
  models.py     Application and History tables
  services.py   perform_action: status change plus history in one transaction
  auth.py       JWT login, demo users
  ai.py         rule flags and Groq call
  main.py       API routes and static file serving
  seed.py       Kannada demo data
  static/       Kannada/English frontend
docs/           plan and workflow notes
```
