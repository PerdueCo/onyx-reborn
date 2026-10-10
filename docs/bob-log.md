# Bob session log — evidence of Bob usage for judging

Copy the template for each session (newest at the bottom).

## Template
### YYYY-MM-DD — Day N
- **Items finished:**
- **Bob modes used:** Ask / Plan / Code (what each was used for)
- **Key prompts:** (1–3, short)
- **What Bob did well / where I corrected it:**
- **Problems + fixes:**
- **Decisions changed:** (D-## in decisions.md)
- **Tests:** pytest result
- **Next item:**
- **Screenshots:** docs/bob-screens/…

---

### 2026-10-0? — Before Day 0 (already done, tool not recorded)
- **Items finished:** Static forensic analysis of the VB4 source →
  `docs/analysis/legacy-inspection-report.md` (inventory, workflows, record layouts, bugs:
  `Len(Query)` 14-byte slot bug, employer State never saved, Hours truncation, unused Date
  field; 10 open questions). Design mockups for landing, login, MFA, student self-service.
  Plan docs: `scope.md`, `prd.md`, `spec.md`, `decisions.md`, `checklist.md`.
  Schema: `docs/design/DATABASE_SCHEMA.md`.
- **Tool used:** Tool not recorded / ChatGPT (schema) / Claude (scope, PRD, spec, checklist,
  legacy report). **This work was NOT done by Bob.** See `AGENTS.md` "Honest credit" section.
- **Next item:** Day 0 — commit, catch-up interview.

---

### 2026-10-09 — Day 0
- **Items finished:**
  1. `AGENTS.md` + all docs committed and pushed — commit `b8f93aa` ("Day 0: plan docs,
     schema, legacy analysis, mockups").
  2. All decisions D-01 through D-26 confirmed by Clarence in `docs/plan/decisions.md`.
  3. `scope.md` corrected — removed "done with Bob" attribution from legacy report reference.
  4. Duplicate mockups deleted: `account login screen-1.png`, `MFA Verification Screen-3.png`.
  5. `docs/bob-log.md` created and populated (this entry).
- **Bob modes used:**
  - Ask mode: read all plan docs (`AGENTS.md`, `scope.md`, `prd.md`, `spec.md`,
    `decisions.md`, `checklist.md`, `DATABASE_SCHEMA.md`, `bob-log.md`); surfaced 5 gap
    questions (D-16 team, D-17 identity provider, D-20 birth data, D-23 roles, D-26 UI flow).
  - Agent mode: ran `git status`/`git log`, committed `AGENTS.md`, updated `decisions.md`,
    fixed `scope.md`, deleted duplicate mockups, wrote this log entry, checked off checklist.
- **Key prompts:**
  - "Start of session. Read AGENTS.md, then docs/plan/scope.md, prd.md, spec.md, decisions.md,
    checklist.md, and the last entry of docs/bob-log.md. Tell me what's done, next item, any
    questions."
  - "Record these answers in decisions.md … Mark other PROPOSED rows CONFIRMED unless you see
    a problem."
- **What Bob did well:** Read all docs, surfaced every open decision, flagged D-18 as
  potentially needing explicit confirmation before marking it CONFIRMED.
- **Where I corrected it:** Clarified that legacy analysis was not Bob's work; instructed
  "don't check off anything you haven't verified."
- **Problems + fixes:** Bob was initially in Ask mode (read-only); switched to Agent mode to
  execute file edits and git commands.
- **Decisions changed:** D-16 (OPEN→CONFIRMED solo), D-17/D-20/D-23/D-26 (PROPOSED→CONFIRMED);
  all other PROPOSED rows also confirmed.
- **Tests:** N/A — no application code yet.
- **Commit IDs:** `b8f93aa` (AGENTS.md + prior docs), `09d9a7a` (Day 0 complete: decisions confirmed, duplicates removed).
- **Next item:** Day 1 — project skeleton: `requirements.txt`, `app/main.py`, uvicorn serves
  "Onyx Reborn" at `/`.

---

### 2026-10-10 — Day 1 (item 1)
- **Items finished:**
  1. Spec §2 typo fixed: `security.py` and `audit.py` moved to `app/` (not `migrations/`); `migrations/` correctly placed at top level.
  2. `onyx.db` (+ shm/wal) added to `.gitignore`.
  3. `.venv` created with `py -3.12`; all packages installed with exact versions pinned in `requirements.txt` (no passlib — using `bcrypt` directly per Clarence's rule).
  4. Full project skeleton created: `app/main.py`, `app/config.py`, `app/db.py`, `app/security.py`, `app/audit.py`, `app/models.py` (stub), `app/routers/` (public, auth, dashboard, students, employment, me, reports, admin), `app/services/` (kpis, legacy_import), `app/templates/` (base.html, public_base.html, public/landing.html, public/about.html), `app/static/css/onyx.css`, `migrations/` (Alembic init + Base wired), `.env.example`, `Dockerfile`, `scripts/seed.py`, `tests/conftest.py`, `tests/test_smoke.py`.
  5. Alembic initialized; `migrations/env.py` wired to `app.db.Base` and reads `DATABASE_URL` from settings.
  6. `pytest -q` → **2 passed**, 1 cosmetic StarletteDep warning (from starlette's own `testclient.py` import; cannot suppress from our side without replacing starlette).
- **Bob modes used:** Agent mode throughout.
- **Key prompts:**
  - "Start of session … Build only Day 1 item 1. Run pytest -q. Check the item off. Then stop."
  - Clarence's rules: py -3.12 only for venv creation; no passlib; bcrypt directly; config.py safe defaults; pin exact versions; onyx.db in .gitignore.
- **What Bob did well:** Created full skeleton in one session; caught Jinja2 API change (new Starlette requires `TemplateResponse(request, name)` not `TemplateResponse(name, {"request": ...})`).
- **Where I corrected it:** Clarence added 5 machine-specific rules before work began.
- **Problems + fixes:**
  - Starlette 1.7 / FastAPI 0.143 changed `TemplateResponse` signature — fixed immediately on first pytest run.
  - `httpx2` does not exist as an installable package; starlette deprecation warning is cosmetic; kept `httpx==0.28.1`.
  - Background commands in PowerShell didn't capture stdout to a file — worked around with `execute_command` direct calls.
- **Decisions changed:** None (confirmed Clarence's 5 machine rules were new constraints, not decision changes).
- **Tests:** `pytest -q` → 2 passed, 0 failed (tests/test_smoke.py — GET / and GET /about both 200).
- **Next item:** Day 1 item 2 — `models.py` per DATABASE_SCHEMA.md + Alembic initial migration + seed roles/permissions (D-23).
