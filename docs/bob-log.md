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

---

### 2026-10-10 — Day 1 (item 2)
- **Items finished:**
  1. `app/models.py` filled with all 12 ORM classes: `UserAccount`, `LocalCredential`,
     `Role`, `UserRole`, `Permission`, `RolePermission`, `Program`, `Student`, `Employer`,
     `Employment`, `ChangeRequest`, `AuditEvent`. All columns, CHECK constraints, FK
     constraints, and `version`/`created_at`/`updated_at` per DATABASE_SCHEMA.md §4-5 +
     spec §3 legacy additions (D-17–D-22). No birth data (D-20). `job_type` includes
     `unknown` (D-22). State saved on Employer (D-06 bug fix).
  2. `migrations/env.py` updated: `render_as_batch=True` in both online and offline modes
     for future SQLite ALTER TABLE support.
  3. Alembic migration `42071248d917_initial.py` generated via `alembic revision
     --autogenerate -m "initial"`. All 12 tables detected. `alembic upgrade head` applied
     cleanly.
  4. `tests/conftest.py` extended with `db_session` fixture: in-memory SQLite, StaticPool
     (every connection shares one DB), `PRAGMA foreign_keys=ON`, `Base.metadata.create_all`,
     rollback after each test.
  5. `tests/test_schema.py` created — 7 tests covering acceptance checks 1, 2, 4:
     - Check 1a: `student_number` UNIQUE constraint enforced
     - Check 1b: `first_name=None` NOT NULL rejected
     - Check 2a: one student holds two simultaneous jobs at different employers
     - Check 2b: same employer, two rows across different date ranges
     - Check 4a: `hours_per_week=-1` CHECK rejected
     - Check 4b: `end_date < start_date` CHECK rejected
     - Check 4c: orphan `Employment` (non-existent student_id) FK rejected
  6. `scripts/seed_roles.py` created — idempotent seeder for 4 roles + 7 permissions +
     13 role-permission assignments per D-23. Verified safe to run twice.
  7. Fixed `tests/conftest.py` name-shadowing bug: `import app.models` collided with
     `from app.main import app`; resolved with `import app.models as _models` and
     `app as fastapi_app` aliases.
- **Bob modes used:** Plan mode (plan file), Agent mode (all code).
- **Key prompts:**
  - "Plan item 2 only now: list files, tests, and how I check it."
  - "OK, approved with these changes: 1. StaticPool + FK pragma … 6. add acceptance check 2 …"
- **What Bob did well:** Generated all 12 ORM classes correctly in one pass; caught the
  `import app` shadowing bug on first pytest run.
- **Where I corrected it:** Clarence added 6 approval conditions (StaticPool, venv paths,
  6th schema test, version columns, render_as_batch, SQLite viewer command).
- **Problems + fixes:**
  - `import app.models` in conftest shadowed `from app.main import app` — the name `app`
    resolved to the package, not the FastAPI instance. Fixed with explicit aliases.
  - `datetime.datetime.utcnow()` deprecation warning — cosmetic, not an error; left as-is
    (changing to `datetime.datetime.now(datetime.UTC)` is a separate cleanup).
- **Decisions changed:** None.
- **Tests:** `pytest -q` → **9 passed**, 0 failed (2 smoke + 7 schema).
- **Commit IDs:** (assigned after push — see next entry)
- **Next item:** Day 1 item 3 — `base.html` sidebar layout + `onyx.css` matching mockups.

---

### 2026-10-10 — Day 1 (item 3)
- **Items finished:**
  1. `app/templates/base.html` — full authenticated layout: fixed navy sidebar (220px),
     inline SVG icons for Overview/Students/Employment/Reports/Administration, active-page
     highlighting (left blue border), sticky top bar with search input + user avatar/name
     area, DEV MODE amber banner when `current_user` is None.
  2. `app/static/css/onyx.css` — full stylesheet rebuilt from mockup tokens: navy `#1b2a4a`,
     blue `#3d6fe8`, page bg `#edf0f7`, white cards (`border-radius:10px`), `active` nav item
     with blue left-border, topbar, search input, user avatar, DEV banner, table styles,
     badge styles (active/inactive/pending/approved/rejected/current), button styles
     (primary/secondary/danger/sm), form styles with focus ring, pagination, public-page
     layout (dark topbar + landing hero), auth card, utility classes.
  3. `app/templates/public_base.html` — updated to navy-topbar + light-bg layout matching
     the welcome screen mockup (wordmark top-left, Sign In button top-right).
  4. `app/templates/public/landing.html` — updated with "A new chapter for student success"
     heading, lead text, arrow CTA button matching the mockup.
  5. `app/templates/dashboard/index.html` — placeholder Overview page using `base.html`:
     4 KPI cards (values `—` until Day 5), Quick links row, System status card.
  6. `app/routers/dashboard.py` — `GET /dashboard` route; `current_user=None` placeholder
     until Day 3 auth is built.
  7. `app/main.py` — dashboard router registered.
  8. `tests/test_smoke.py` — added `test_dashboard_ok` asserting 200, "Overview" in body,
     "sidebar" class present, "DEV MODE" banner present.
- **Bob modes used:** Agent mode throughout. Read all 4 mockup PNG files before coding.
- **Key prompts:**
  - "Go for item 3: sidebar layout … navy left sidebar … Use .venv\\Scripts\\ commands only."
- **What Bob did well:** Extracted exact design tokens from mockup images (navy, blue, page
  bg, card radius, active nav style) before writing a single line of CSS.
- **Where I corrected it:** No corrections needed this session.
- **Problems + fixes:** None — 10 passed on first run.
- **Decisions changed:** None.
- **Tests:** `pytest -q` → **10 passed**, 0 failed.
- **Next item:** Day 1 Students — list/search, add form, edit form; STU number generated and
  immutable; required-field validation; acceptance checks 1 and 4 in router tests.

---

### 2026-10-11 — Day 2 (welcome page + planning)
- **Items finished:**
  1. Welcome page redesigned to match `expected-welcome.png` (desktop) and
     `expected-welcome-responsive.png` (mobile) — three iterations:
     - Iteration 1 (`fb560dc`): two-column CSS grid, hand-built SVG/HTML illustration,
       responsive collapse at 900 px, `clamp(44px,6vw,88px)` headline, focus ring,
       reduced-motion guard, footer border + left-align, 11 tests.
     - Iteration 2 (`b4d2d49`): replaced hand-built illustration with
       `welcome-illustration-desktop.png` / `welcome-illustration-mobile.png` from
       `app/static/img/`; loaded Inter from Google Fonts (400/500/700/800); headline
       `clamp(44px,5.6vw,92px)` / weight 800 / letter-spacing −0.035em / line-height 1.02;
       subheading #3B5378 clamp(22px,2.3vw,38px) weight 500; support line #5B6782 24px;
       CTA button 390 px × 76px radius 12px #1F6FEB; topbar 92px, logo 40px; footer
       border-top #DCE2EC, 40px padding, 26px wordmark; mobile: gray subheading 26px,
       full-width 64px button, centered footer "BSSI Modernization".
     - `c7ad9f3`: added three checklist lines (welcome page done + Oct 11 checkpoint note).
  2. **Oct 11 checkpoint** — scope cut recorded as D-27 in `decisions.md`: student portal
     OUT, review queue OUT, admin user UI OUT, audit viewer OUT, reports cut to 1 + CSV.
  3. `checklist.md` rewritten as a clean 5-day sprint (Mon 13 → Fri 17) with roadmap
     section for cut items.
- **Bob modes used:**
  - Plan mode: wrote `docs/plan/welcome-page-redesign-plan.md` with gap analysis (8 diffs
    listed) and 3 sub-tasks before any code was written.
  - Agent mode: all CSS/HTML/test changes across 3 iterations; read both PNG mockups before
    each iteration; ran `pytest -q` after every change.
- **Key prompts:**
  - "Plan an update to the welcome page … Compare them to the current page and list every
    difference … List the files you will change … Wait for my OK."
  - "Fix the welcome page to match … ILLUSTRATION: Replace … with images … FONT: Load Inter
    … DESKTOP … MOBILE …" (full pixel-precise spec from Clarence).
  - "End of session. Do these steps: 1. Mark done … 3. Rewrite checklist.md as a 5-day plan …"
- **What Bob did well:** Read both PNG mockups before planning; listed every gap before
  touching code; handled all 3 iterations cleanly in one prompt each.
- **Image-crop decision:** Clarence provided the illustration as pre-cropped PNGs
  (`app/static/img/welcome-illustration-desktop.png`, `…-mobile.png`) rather than having
  Bob re-build it in HTML/CSS. Bob switched to `<img>` tags accordingly. This was a
  Clarence-directed decision, not a Bob guess.
- **Where I corrected it:**
  - Iteration 1: Clarence added 4 approved-with-changes conditions (clamp instead of jump,
    button max-width 100%, illustration scale at 901–1200 px, keep /about unbroken).
  - Iteration 2: full pixel-spec override (topbar 92px, Inter weights, exact colors, button
    76px, footer 40px padding) — Bob had the right structure but wrong token values.
  - Test fix: `<br>` in headline broke the existing `"A new chapter for student success"`
    assertion — fixed by splitting into two separate checks.
- **Problems + fixes:**
  - `test_landing_headline` failed on first pytest after adding `<br>` — string "A new
    chapter for student success" no longer appears verbatim in HTML. Fixed by splitting
    assertion into "A new chapter for" + "student success" checks.
  - `git push` for commit `c7ad9f3` failed with "Could not resolve host: github.com"
    (DNS/network drop). Push carried over to this session's final commit.
- **Decisions changed:** D-27 added (Oct 11 checkpoint scope cuts — see above).
- **Tests:** `pytest -q` → **11 passed**, 0 failed (3 smoke + 7 schema + 1 headline).
- **Commit IDs:** `fb560dc` (welcome page v1), `b4d2d49` (welcome page v2 — exact illustration
  + type), `c7ad9f3` (checklist lines added).
- **Next item:** Day 1 Mon Oct 13 — Students list + search + add + edit (acceptance checks
  1 and 4); then 1998 importer; then demo seed with ~250 fictional students.

---

### 2026-10-11 — Step 3 (legacy import + demo data)

- **Items finished:**
  1. `app/services/legacy_import.py` — full spec §5 implementation: cp1252 decode,
     fixed-width field parsing with module-level assert guards (357 / 238 bytes),
     SS_Number read-and-discard, Month/Day discarded (D-20), YesNo Y/N/0/1 mapping,
     2-digit year pivot, Amount→Decimal, employer upsert by legacy_code,
     start_date=enrolled_date (D-21), job_type='unknown' (D-22), idempotent
     (first+last+home_phone+legacy_source guard), audit event written.
  2. `scripts/seed_demo.py` — 250 fictional students across 5 programs, 12 demo
     employers (including dashboard-mockup names), 183 jobs: 17 students with 2
     concurrent jobs (34 rows), 99 single current, 50 single ended, 40 seeking.
     Idempotent via DEMO_SEED marker employer. RNG seeded deterministically.
  3. `scripts/reset_db.py` — one-command reset: deletes SQLite file (disposing
     engine first to release Windows lock), runs `alembic upgrade head`, seeds
     roles, imports 1998 data, seeds demo, creates 2 demo users, prints sign-in
     credentials.
  4. `tests/test_import.py` — 11 tests: width sums, 5+5 import, 5 jobs, idempotent,
     no SSN in DB, enrolled_date parsed, YesNo mapped, job_type=unknown, start_date
     equals enrolled_date, audit event written.
- **Bob modes used:** Agent mode throughout.
- **Key prompts:**
  - "Run-sheet step 3: 1998 import + demo data. First, in 3 lines max, tell me which
    step-2 Students items are missing. Then build: 1. legacy_import.py … 2. seed_demo.py
    … 3. reset_db.py … Tests: widths sum to 357/238; 5+5 imported; run twice adds nothing;
    no SSN digits in DB. Run pytest, run reset_db.py, commit, push."
- **What Bob did well:** Read all 5 legacy data records and both file layouts before
  writing a single line; confirmed field widths sum correctly; caught Windows file-lock
  issue on reset_db.py and fixed with engine.dispose() + retry.
- **Where I corrected it:** No corrections from Clarence in this session.
- **Problems + fixes:**
  - `reset_db.py` first run failed with `PermissionError: [WinError 32]` because
    pytest's TestClient held an open handle to `onyx.db`. Fixed by calling
    `engine.dispose()` before deleting the file, with a 5-attempt retry loop.
  - `print()` with Unicode box-drawing chars raised `UnicodeEncodeError` on Windows
    PowerShell (cp1252 codec). Replaced with ASCII dashes.
- **Decisions changed:** None.
- **Tests:** `pytest -q` → **36 passed**, 0 failed (11 new import tests + 25 existing).
- **Commit ID:** `efedd26`
- **DB totals after reset_db.py:**
  - **255 students** (5 legacy + 250 demo)
  - **188 jobs** (5 legacy + 183 demo)
- **Next item:** Day 1 Students list + search + add + edit (checklist item still open).
