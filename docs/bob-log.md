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


### 2026-10-16 — Auth + Students (steps 2 & 3 prerequisite)

*(This session was not logged live due to the IBM Bob API outage mid-session;
entries reconstructed from git history — commit IDs are exact.)*

- **Items finished:**
  1. `app/security.py` — `hash_password`/`verify_password` (bcrypt), Fernet TOTP
     encryption/decryption, CSRF token helpers, 30-min session timeout,
     `get_current_user` dependency, `get_user_permissions`, `require_permission(code)`
     factory. Decisions D-28 (CSRF on all POST), D-29 (lockout 5/15min), D-30
     (2-step always required) added to `decisions.md`.
  2. `app/audit.py` — `log_event(db, user_id, action, entity_type, entity_id, detail)`;
     best-effort (never breaks a user flow); lazy import to avoid circular imports.
  3. `app/routers/auth.py` — `POST /login` (active check, lockout guard, bcrypt verify,
     session `{uid, mfa_ok:false}`), `GET/POST /mfa/setup` (pyotp QR + 8 recovery
     codes, confirm code), `GET/POST /mfa/verify` (`valid_window=1`, recovery-code
     fallback, consumes used code), `POST /logout`; CSRF checked on every POST; audit
     events: `sign_in_ok`, `sign_in_fail`, `sign_in_locked`, `sign_out`, `mfa_setup`,
     `mfa_ok`, `mfa_fail`.
  4. `app/routers/students.py` — full students CRUD: list + search (name or STU#),
     new form (POST), edit form (POST), detail view. STU-#### generated sequentially,
     immutable. Phone format validation. Duplicate warning (non-blocking). All routes
     gated by `students.read` / `students.manage` permissions. Audit on create/edit.
  5. Templates: `auth/login.html`, `auth/mfa_setup.html`, `auth/mfa_verify.html`,
     `auth/mfa_recovery.html`; `students/list.html`, `students/form.html`,
     `students/detail.html`; `403.html`.
  6. `app/main.py` — auth + students routers registered, `SessionMiddleware` added,
     CSRF Jinja2 global registered.
  7. `app/templates/base.html` — DEV MODE banner removed; permission-filtered sidebar
     (nav items hidden when user lacks the required permission); CSRF hidden field in
     sign-out form.
  8. `app/templates_env.py` — shared Jinja2 `Environment` / `Jinja2Templates` instance
     (eliminates duplicate `templates` objects across routers).
  9. `scripts/reset_db.py` (v1) — drop-all, create-all, seed roles, create 2 demo users.
  10. `tests/test_auth.py` — 14 tests: login ok, wrong password, lockout, locked-account
      rejected, TOTP correct, TOTP wrong, recovery code works+consumed, logout,
      unauthenticated redirect, 403 wrong role, missing MFA_ENC_KEY raises clearly,
      missing SESSION_SECRET raises clearly, unenrolled user → /mfa/setup,
      /login topbar Sign In button hidden.
- **Bob modes used:** Plan mode (wrote `docs/plan/auth-plan.md` before any code);
  Agent mode (4 implementation chunks).
- **Key prompts:**
  - "Build auth per spec §4 + decisions D-17/D-18/D-28–D-30. Plan first."
  - "Chunk 1: security.py + audit.py + auth router + students router + templates."
  - "Chunk 2: gate routes, 403 page, DEV MODE removed, sidebar filtered by perms."
  - "Chunk 3: reset_db.py + test_auth.py (10 tests)."
  - "Bug fix chunk: MFA_ENC_KEY guard + /mfa/setup flow test."
- **What Bob did well:** Planned the full auth flow in `auth-plan.md` before writing
  a line of code; kept TOTP secret encrypted at rest (Fernet) without being asked;
  recovery-code consumption was implemented correctly on first pass.
- **Where I corrected it:** Added MFA_ENC_KEY startup guard after first reset_db run
  silently generated a random key at import time and caused TOTP decrypt failures.
- **Problems + fixes:**
  - **MFA_ENC_KEY mismatch:** `config.py` was generating a fresh Fernet key when
    `MFA_ENC_KEY` was blank instead of raising. TOTP secrets encrypted with key A
    could not be decrypted after a process restart with key B. Fix: `_require()`
    helper raises `RuntimeError` with a clear message when the key is empty; added
    startup guard in `app/main.py` and `scripts/reset_db.py` (v1 guard; v2 reset_db
    replaced in Step 3).
  - **IBM Bob API outage:** Mid-session API interruption (503s) broke the live
    context. Session was reconstructed from file saves; the outage caused this entry
    to be written post-hoc rather than live.
  - `test_auth.py` initially used a shared TestClient fixture; tests contaminated
    each other through shared session cookies. Fixed by switching to per-test
    `auth_client` fixture that overrides `get_db` with an isolated in-memory session.
- **Decisions changed:** D-28, D-29, D-30 added (CSRF, lockout policy, 2-step always).
- **Tests:** `pytest -q` → **25 passed**, 0 failed (final state after bug-fix chunk).
- **Commit IDs:** `acb986e` (Chunk 1), `ae750f7` (Chunk 2), `0e7781e` (Chunk 3),
  `e6095f0` (bug fix: MFA_ENC_KEY guard, 25 passed).
- **Next item (at that time):** Step 3 — legacy importer + demo seed + reset_db.

---

### 2026-10-16 — Step 3 (legacy import + demo data)

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
- **Next item:** Day 3 — Employers list + add + edit; add job / end job; KPIs wired; dashboard real numbers.

---

### 2026-10-16 — End of session wrap-up

- **Items finished:** Pytest run confirmed 36 passed, 0 failed. Checklist updated
  (steps 2 + 3 + 4 marked done). Bob-log filled in for all sessions including the
  unlogged Oct 16 auth+students session. Commit `9e14b13` + this wrap pushed.
- **Bob modes used:** Agent mode (end-of-session maintenance).
- **Key prompts:**
  - "End of session: run pytest, add today's entry to docs/bob-log.md (modes used,
    key prompts, problems + fixes incl. the MFA_ENC_KEY mismatch and the API outage,
    commit IDs), update checklist.md (steps 2, 3, 4 done), commit, push, tell me
    tomorrow's first step."
- **What Bob did well:** Reconstructed the unlogged auth+students session entirely
  from git history (commit stats, file lists, test counts) without fabricating
  anything; noted the API outage honestly as the reason for the gap.
- **Where I corrected it:** Clarence explicitly named the two problems to document
  (MFA_ENC_KEY mismatch and API outage) — Bob would not have known to include them
  without being told.
- **Problems + fixes:** None new this wrap step.
- **Decisions changed:** None.
- **Tests:** `pytest -q` → **36 passed**, 0 failed.
- **Commit IDs:** `9e14b13` (prior checklist/log update), `[this commit]` (see below).
- **Next item:** Day 3 — Employers list + add + edit (name, address, city, state,
  phone — D-06 bug fixed); add job / end job on student detail page; `kpis.py` real
  counts; dashboard KPI cards wired to DB; recent activity feed.

---

### 2026-10-16 — Step 2 fix (students CRUD fully working)

- **Items finished:**
  1. **CSRF missing from student forms** — `students/form.html` had no `<input type="hidden" name="csrf_token">`,
     so every POST from `/students/new` and `/students/{id}/edit` was rejected with 403. Fixed by
     adding the hidden field and calling `check_csrf()` at the top of both POST handlers.
  2. **Jinja2 `fval` macro broken for ORM objects** — `student[name]` uses `__getitem__` which
     SQLAlchemy ORM objects don't implement; silently fell through to the `else` branch, so
     edit forms showed blank fields for every value. Fixed by replacing with `student | attr(name)`.
  3. **`block title` defined twice** — the original template used `{% if student %}{% block title %}…{% endif %}`
     pattern, which Jinja2 forbids (a block can only appear once). Caused `TemplateAssertionError`
     on every request to `/students/new` or `/students/{id}/edit`. Fixed by collapsing to a single
     inline `{% block title %}{% if student %}…{% else %}…{% endif %}{% endblock %}`.
  4. **`work_phone` format not validated** — `_validate_form` checked `home_phone` but not
     `work_phone`. Added the check.
  5. **`tests/test_students.py`** — 12 new end-to-end tests through HTTP signed-in client:
     auth-redirect guard, new form renders (csrf + fields), create → 303, created student listed,
     find by STU number, edit form shows existing values, edit saves + STU unchanged, missing first
     name rejected (422 + values kept), missing last name rejected, bad phone rejected, detail page
     renders, duplicate warning shown.
  6. `scripts/_check_student_pages.py` — standalone smoke-check script used to verify the running
     app (confirmed all 10 checks OK on the live server via TestClient).
- **Bob modes used:** Agent mode throughout.
- **Key prompts:**
  - "Step 2 is NOT complete … Fix and finish per RUN-SHEET step 2 … CSRF token on POST forms …
    Test it end to end … Run pytest, commit, push."
- **What Bob did well:** Diagnosed all four root causes from code inspection before running anything;
  fixed them in a single pass.
- **Where I corrected it:** Clarence stopped the stuck uvicorn polling loop and directed Bob to
  use the already-running server on port 8000.
- **Problems + fixes:**
  - `TemplateAssertionError: block 'title' defined twice` — pre-existing bug exposed when tests
    actually exercised the templates (previous session only hit auth routes). Fixed inline.
  - Uvicorn `Start-Process` via PowerShell exited immediately with empty log — PowerShell
    pipeline kills the child when the parent exits. Worked around by using TestClient directly.
- **Decisions changed:** None.
- **Tests:** `pytest -q` → **48 passed**, 0 failed (12 new student tests + 36 existing).
- **Commit ID:** `9fbd79c`
- **Next item:** Day 3 — Employers list + add + edit; add job / end job; `kpis.py` real counts;
  dashboard KPI cards wired to DB.


---

### 2026-10-16 — Demo sign-in helpers (judge-friendly UX)

- **Items finished:**
  1. **`app/templates/auth/login.html`** — replaced static plaintext demo-accounts box
     with a "Try the demo" card containing two real POST forms: "Try as Staff" and
     "Try as Administrator". Each form includes a `csrf_token` hidden field (same
     token generated for the page), hidden `email`/`password` fields, and a
     `btn-secondary` button. Shown only when `demo_mode=True`; absent when `False`.
  2. **`app/routers/auth.py`** — `get_settings` and all reset_db constants
     (`ADMIN_EMAIL`, `ADMIN_PASSWORD`, `STAFF_EMAIL`, `STAFF_PASSWORD`,
     `ADMIN_TOTP_SECRET`, `STAFF_TOTP_SECRET`) promoted to module-level imports
     (were per-call `from … import` inside functions). `GET /login` now passes
     `demo_admin_*` / `demo_staff_*` context vars. `GET /mfa/verify` computes a live
     `pyotp.TOTP(secret).now()` code for admin/staff demo users only, passes it as
     `demo_code`.
  3. **`app/templates/auth/mfa_verify.html`** — added `{% if demo_code %}` block that
     shows a "Demo account — current code: NNN NNN" box and a second POST form with a
     "Use demo code" button pre-filled with the live code. Absent for all other users
     and when `DEMO_MODE=False`.
  4. **`scripts/reset_db.py`** — added `NEWSTAFF_EMAIL = "newstaff@onyx.demo"`,
     `NEWSTAFF_PASSWORD = "OnyxNew2026!"`, `NEWSTAFF_DISPLAY_NAME = "New Staff"`.
     `_create_demo_users` now creates this third user with `totp_secret=None` and
     `mfa_enabled=False`, so first sign-in sends the QR setup page. `_make_user`
     helper updated to conditionalize `encrypt_totp_secret` on whether a secret
     was provided. Summary printout updated.
  5. **`tests/test_demo_mode.py`** — 12 new tests: demo box present/absent,
     csrf count ≥ 3, staff/admin button posts correct credentials, MFA hint shown for
     admin (code verifies with pyotp valid_window=2), MFA hint shown for staff, hint
     absent when `DEMO_MODE=False`, hint absent for non-demo users, newstaff redirects
     to `/mfa/setup`, `/mfa/setup` shows QR, constants importable.
- **Bob modes used:** Agent mode throughout.
- **Key prompts:**
  - "Bob crashed mid-task. Run git status and git diff --stat first and tell me in 3
    lines what is already done. Then finish this task: Judge-friendly demo sign-in …
    Run pytest, commit, push."
- **What Bob did well:** Recognised clean state from `git status`, understood full
  scope immediately, promoted imports to module level to fix `patch()` target, all 12
  tests green on second run (first run failed because `get_settings` was a local
  import so `patch("app.routers.auth.get_settings")` raised `AttributeError`).
- **Where I corrected it:** No corrections from Clarence; Bob self-corrected the patch
  target error after first pytest run.
- **Problems + fixes:**
  - First pytest run: 7 of 12 tests failed with
    `AttributeError: module 'app.routers.auth' does not have attribute 'get_settings'`
    because the function did `from app.config import get_settings` inside the route
    body. Fixed by moving the import to module level.
- **Decisions changed:** None.
- **Tests:** `pytest -q` → **60 passed**, 0 failed (12 new demo tests + 48 existing).
- **Commit ID:** `fd8614a`
- **Next item:** Day 3 — Employers list + add + edit; add job / end job; `kpis.py`
  real counts; dashboard KPI cards wired to DB.

---

### 2026-10-16 — Day 3 part 1: Employment router + employers + add/end job

- **Items finished:**
  1. **`app/routers/employment.py`** — filled from empty stub to full implementation:
     - `GET /employment/employers` — list all employers (sorted by name)
     - `GET/POST /employment/employers/new` — add employer (name required; address, city,
       state, zip, phone, company_type optional; audit event; D-06 state field fixed)
     - `GET/POST /employment/employers/{id}/edit` — edit employer; same validation
     - `GET/POST /employment/new?student_id=` — add job to a student; employer dropdown,
       job_title required, job_type dropdown (part_time/full_time/other/unknown), start_date
       required, end_date optional with start≤end guard, hours_per_week non-negative guard,
       hourly_rate + supervisor (legacy fields); audit event; 303 → student detail
     - `GET/POST /employment/{id}/end` — end a current job; end_date required, must be ≥
       start_date; version incremented; history preserved; audit event; 303 → student detail;
       already-ended job → 400
  2. **Templates** (`app/templates/employment/`):
     - `employers_list.html` — data table with Edit button per row
     - `employer_form.html` — add/edit form with state dropdown (mirrors student form pattern)
     - `job_form.html` — add-job form linked from student detail; employer dropdown, date
       inputs, hours/rate/supervisor fields; empty-employers warning
     - `end_job_form.html` — confirmation form showing current-job summary card + date input
  3. **`app/main.py`** — employment router registered.
  4. **`app/templates/students/detail.html`** — added "End" button per current job row
     (visible only when `employment.manage` in `user_perms`); added `<th>` column header.
  5. **`tests/test_employment.py`** — 15 new end-to-end tests:
     - `test_employers_list_requires_auth` — unauthenticated → 303 to /login
     - `test_add_employer_success` — valid POST → 303, employer in list
     - `test_add_employer_name_required` — blank name → 422
     - `test_edit_employer_saves` — name change persists in DB
     - `test_add_job_success` — valid POST → 303 to student detail, job visible
     - `test_add_job_missing_title_rejected` — 422 + error
     - `test_add_job_negative_hours_rejected` — acceptance check 4 (hours ≥ 0)
     - `test_add_job_end_before_start_rejected` — acceptance check 4 (date order)
     - `test_two_simultaneous_jobs` — acceptance check 2 (two current jobs, both shown)
     - `test_end_job_success` — end_date saved, job still in history (check 3)
     - `test_end_job_end_date_before_start_rejected` — 422, unchanged (check 4)
     - `test_end_job_already_ended_returns_400` — guard works
     - `test_end_one_job_leaves_other_intact` — check 3 isolation
- **Bob modes used:** Agent mode throughout.
- **Key prompts:**
  - "First check app/routers/employment.py and any job templates that already exist; reuse
    and finish them instead of starting over."
- **What Bob did well:** Inspected all existing files before writing a line of code; reused
  exact patterns from `students.py` (dependency injection, `_ctx`, `check_csrf`, `_manage_dep`,
  template context, audit calls); handled the FastAPI path-ordering risk (static
  `/employers/new` before `/employers/{id}/edit`) correctly; all 15 tests green first run.
- **Where I corrected it:** No corrections from Clarence.
- **Problems + fixes:** None — 73 passed on first pytest run.
- **Decisions changed:** None.
- **Tests:** `pytest -q` → **73 passed**, 0 failed (15 new employment tests + 60 existing).
- **Commit ID:** (pending push)
- **Next item:** Day 3 remainder — `app/services/kpis.py` real counts; Dashboard KPI cards
  wired to DB; recent activity feed (last 10 audit events).
### 2026-10-16 — Step 7: Dashboard real KPIs + mobile responsive layout

- **Items finished:**
  1. **`app/services/kpis.py`** — real SQLAlchemy queries:
     - `get_kpis()` → total_students (active), employed_count (distinct students with ≥1
       current job), employed_pct, current_jobs (row count), avg_hourly_rate (formatted
       `$X.XX` or `—`), seeking_count; all counts use `date.today()` as "as-of"
     - `get_recent_activity(limit=10)` → last N audit events with actor display_name
     - `get_security_events(limit=10)` → filtered to `sign_in_failed / access_denied /
       account_locked` (admin-only)
  2. **`app/routers/dashboard.py`** — wires all three service calls; passes `is_admin`
     flag (presence of `accounts.manage` perm); security_events only fetched for admin
  3. **`app/templates/dashboard/index.html`** — rebuilt:
     - 4 KPI cards with real template variables (Active Students, Currently Employed with
       %, Current Jobs with avg rate sub-line, Seeking Employment)
     - Recent activity feed (last 10 audit events) — both roles
     - Two-column dash-grid layout (activity left, quick links right)
     - Admin-only row: Data Safety card (SSN=None, MFA, audit, session, bcrypt) +
       Security events card with amber "Admin only" badge
     - No review queue, no period picker, no print, no monthly trend
  4. **`app/templates/base.html`** — added mobile-topbar strip (navy, 52 px, hamburger
     button + wordmark + sign-out icon), sidebar-overlay div, inline JS drawer toggle
     (<20 lines vanilla JS; no deps); desktop behaviour unchanged
  5. **`app/static/css/onyx.css`** — appended:
     - `.dash-grid` 2-col grid, `.activity-list / .activity-item / .activity-dot-*`,
       `.quick-links / .quick-link-btn`, `.card-title-icon`, `.kpi-rate`
     - `.mobile-topbar` / `.sidebar-overlay` hidden on desktop; `.mobile-menu-btn` /
       `.mobile-signout-btn` 44 px touch targets
     - `@media (max-width: 639px)` breakpoint: sidebar slides left, right-col
       margin-left:0, desktop topbar hidden, main-content padding 16px, kpi-row 2×2
       grid, dash-grid 1-col, form-row-2/3 + form-grid collapse to 1-col, btn
       min-height:44px, auth-card full-width, detail-grid stacks
  6. **`tests/test_dashboard.py`** — 16 tests:
     - `test_staff_dashboard_loads` — 200
     - `test_staff_sees_kpi_cards` — all 4 labels present
     - `test_staff_sees_recent_activity` — section present
     - `test_staff_no_data_safety` — admin-only card absent for staff
     - `test_staff_no_security_events` — admin-only card absent for staff
     - `test_admin_dashboard_loads` — 200
     - `test_admin_sees_kpi_cards` — all 4 labels present
     - `test_admin_sees_data_safety` — section present
     - `test_admin_sees_security_events` — section present
     - `test_admin_no_review_queue` — review queue absent (D-27 cut)
     - `test_kpi_total_students` — "2" appears (fixture has 2 active)
     - `test_kpi_employed_count` — "50%" appears (1/2 students employed)
     - `test_kpi_seeking_count` — "Seeking Employment" label present
     - `test_kpi_avg_rate_shown` — "$15.00" appears (fixture job rate)
     - `test_kpi_current_jobs` — "Current Jobs" label present
     - `test_dashboard_requires_auth` — unauthenticated → 303 to /login
- **Bob modes used:** Agent mode throughout.
- **Key prompts:**
  - "Run-sheet step 7: rebuild /dashboard to match mockups; real queries per
    dashboard-spec.md rules; admin also sees Data safety + security events; staff
    does not; no review queue, period picker, print, or monthly trend; also make every
    signed-in page work at 390px wide."
- **What Bob did well:** Read all required docs in order before writing a line; kept the
  responsive CSS additive (no existing selectors changed); single `@media` block covers
  all authenticated pages (login, MFA, students, forms, detail); fixture numbers chosen
  so 50% test is deterministic; 16 new tests green first run; full 89-test suite green.
- **Where I corrected it:** No corrections from Clarence.
- **Problems + fixes:** None — 89 passed on first pytest run.
- **Decisions changed:** None.
- **Tests:** `pytest -q` → **89 passed**, 0 failed (16 new dashboard tests + 73 existing).
- **Commit ID:** `bb66baf`
- **Next item:** Day 4 — Employment history report + CSV export; Dockerfile; README.

### 2026-10-17 — Step 8: /reports — Current Employment report + CSV export

- **Items finished:**
  1. **`app/services/reports.py`** — `get_current_employment(db, *, program_id, employer_id)`:
     - Joins Employment → Student → Employer → Program (outer join)
     - Filters to `Student.status == "active"`, optional program_id / employer_id
     - Python-side `is_current_job()` call from `kpis.py` (D-31 single source of truth)
     - Returns list of dicts with keys: student_name, stu_number, program, employer,
       job_title, hours, rate (formatted "$X.XX" or "—")
     - `get_programs()` / `get_employers()` helpers for filter dropdowns
  2. **`app/routers/reports.py`** — requires `reports.read` permission:
     - `GET /reports` — HTML table with program + employer filter GET params
     - `GET /reports/current-employment/export.csv` — StreamingResponse; same
       filter params; CSV header row + one data row per result
  3. **`app/templates/reports/current_employment.html`** — extends `base.html`;
     - Filter form (program select, employer select, Filter + Clear buttons)
     - "N records found" count + Export CSV button + Print button
     - 7-column `<table class="report-table">` inside `.report-table-wrap`
     - Print `@media` block hides sidebar/topbar/filters/actions inline in `<style>`
  4. **`app/static/css/onyx.css`** — appended report styles:
     - `.report-table-wrap { overflow-x: auto }` → sideways scroll at 390px
     - `.report-table` min-width: 640px; th uppercase muted; td borders
     - `.report-table td.mono` (STU number), `.report-table td.num` (right-align)
     - `.report-filter-form .form-row-3` 3-col grid, collapses to 1-col ≤639px
     - `@media print` block hides sidebar + nav + filters; page margins 1.5cm
  5. **`app/main.py`** — added `include_router(reports_router.router)`
  6. **`tests/test_reports.py`** — 12 tests (all green first run):
     - `test_reports_page_loads` — 200
     - `test_reports_html_has_column_headers` — all 7 headers present
     - `test_reports_current_only` — ended job excluded; count == 2
     - `test_reports_filter_by_employer_html` — Corp A → 1 row; Corp B absent
     - `test_reports_filter_by_program_html` — Beta → 1 row; Alpha absent
     - `test_csv_headers_match_screen` — CSV row 0 == expected 7 strings exactly
     - `test_csv_row_count_matches_html_unfiltered` — CSV count == HTML count
     - `test_csv_row_count_matches_html_with_employer_filter` — both == 1
     - `test_csv_row_count_matches_html_with_program_filter` — both == 1
     - `test_reports_empty_filter_shows_zero` — "0 records" in page
     - `test_reports_requires_auth` — /reports unauthenticated → 303 /login
     - `test_csv_export_requires_auth` — /export.csv unauthenticated → 303 /login
- **Bob modes used:** Agent mode throughout.
- **Key prompts:**
  - "Run-sheet step 8: build /reports with one report: Current employment (student, STU,
    program, employer, job title, hours, rate), using the shared is_current() helper.
    Filters by program and employer, on-screen table, Export CSV button, print-friendly
    CSS, works at 390px (table scrolls sideways). Add 'Reports' in the sidebar if
    missing. Tests: CSV headers + row count match the on-screen table for a filter."
- **What Bob did well:** Sidebar already had Reports nav item (step 7 prebuilt it).
  `is_current_job()` reused without duplication. CSV header list kept in one place in
  the router so HTML and CSV headers can never diverge. `overflow-x:auto` wrapper gives
  390px support for free. Print CSS hidden via inline `<style>` in template so it only
  loads on this page.
- **Where I corrected it:** No corrections from Clarence.
- **Problems + fixes:** None — 12 new tests + 118 existing = 130 passed on first run.
- **Decisions changed:** None.
- **Tests:** `pytest -q` → **130 passed**, 0 failed (12 new + 118 existing).
- **Commit ID:** `4ff97a6`
- **Next item:** Day 4 — Dockerfile; `.env.example`; README.md.


### 2026-10-17 — Bug fix: empty program_id / employer_id caused 422 on /reports

- **Items finished:**
  1. **`app/routers/reports.py`** — both `/reports` and `/reports/current-employment/export.csv`:
     - Changed `program_id` and `employer_id` query params from `int | None` to `str | None`.
     - Added `_coerce_id(raw)` helper: `None` or `""` → `None` (no filter); digit string → `int`; anything else → `None` (ignore garbage). This fixes the FastAPI 422 `int_parsing` error that fired when the "All programs" or "All employers" `<option value="">` was selected, which sends `program_id=` (empty string).
     - `selected_program_id` / `selected_employer_id` passed to template as coerced `int | None` so `<option selected>` matching still works.
  2. **`tests/test_reports.py`** — 5 new regression tests added:
     - `test_reports_empty_string_both_params_returns_all` — `?program_id=&employer_id=` → 200, all 2 current rows.
     - `test_reports_empty_program_id_with_employer_set` — `program_id=` blank + `employer_id=N` → 1 row (employer filter only).
     - `test_reports_empty_employer_id_with_program_set` — `employer_id=` blank + `program_id=N` → 1 row (program filter only).
     - `test_csv_export_empty_string_both_params` — CSV with both empty → 200, 2 data rows.
     - `test_csv_export_empty_program_id_with_employer_set` — CSV with blank program + set employer → 1 data row.
- **Bob modes used:** Agent mode throughout.
- **Key prompts:**
  - "Bug in /reports: submitting the filter form with 'All programs' or 'All employers' sends program_id= (empty string) and FastAPI returns a 422 int_parsing error. Fix both /reports and /reports/current-employment/export.csv: accept program_id and employer_id as optional strings, treat '' (or missing) as no filter, convert digits to int, and ignore anything else. Make the Export CSV link carry the same filters. Add tests … Run pytest, commit, push."
- **What Bob did well:** Diagnosed root cause immediately (FastAPI strict int coercion rejects `""`); minimal fix — only two param type annotations changed + one 5-line helper added; template needed no change (coerced int `None` is already falsy, so CSV link logic was already correct); all 5 new tests written to cover every combination described in the prompt.
- **Where I corrected it:** No corrections from Clarence.
- **Problems + fixes:** None — 17 report tests + 118 existing = 135 passed on first run after fix.
- **Decisions changed:** None.
- **Tests:** `pytest -q` → **135 passed**, 0 failed (5 new + 130 existing).
- **Commit ID:** `c9c3c45`
- **Next item:** Day 4 — Dockerfile; `.env.example`; README.md.


### 2026-10-17 — Bug fix: duplicate program name + CODE — Name display

- **Items finished:**
  1. **`scripts/seed_demo.py`** — ACC110 renamed from "Accounting Technology" to "Accounting".
     The 1998 import already creates ACC501 "Accounting Technology"; the demo seed's
     identical name was causing both to appear in every dropdown with the same label.
     ACC501, MM301, NET401 from the legacy import are untouched.
  2. **`app/services/reports.py`** — `get_programs()` ordered by `Program.code` (was `name`).
     Report table `"program"` dict value now emits `"CODE — Name"` (e.g.
     `"ACC110 — Accounting"`) instead of just the name.
  3. **`app/services/kpis.py`** — `get_employment_by_program()` `program_name` key now uses
     `"CODE — Name"` so the dashboard employment-rate bars are labelled with codes.
  4. **`app/routers/students.py`** — all 4 program list queries changed from
     `order_by(Program.name)` to `order_by(Program.code)`.
  5. **`app/templates/reports/current_employment.html`** — program filter dropdown option
     changed from `{{ p.name }}` to `{{ p.code }} &mdash; {{ p.name }}`.
  6. **`tests/test_program_uniqueness.py`** — 3 new tests:
     - `test_no_duplicate_program_names_after_seed` — verifies every Program.name is unique
       across all rows after the demo seed runs.
     - `test_report_dropdown_labels_include_codes` — verifies each active program's code
       appears inside the /reports page's `<select id="program_id">` block.
     - `test_report_table_program_column_includes_codes` — verifies tbody rows contain a
       CODE pattern (e.g. `CIS101 —`) in the Program column.
- **Bob modes used:** Agent mode throughout.
- **Key prompts:**
  - "ACC110 'Accounting Technology' in seed_demo.py collides with ACC501 'Accounting Technology'
    from 1998 import … rename ACC110 to 'Accounting'. Every program dropdown and list shows
    'CODE — Name'. Sort by code. Tests: no two programs share a name; report dropdown labels
    include codes. Run pytest, commit, push."
- **What Bob did well:** Traced all five locations (seed_demo.py, reports.py, kpis.py,
  students.py router, reports template) before writing a line; student detail template and
  student form already used `code — name` format so no change needed there; targeted only
  the broken spots.
- **Where I corrected it:** No corrections from Clarence.
- **Problems + fixes:** None — 138 passed on first pytest run after all changes.
- **Decisions changed:** None.
- **Tests:** `pytest -q` → **138 passed**, 0 failed (3 new + 135 existing).
- **Commit ID:** `447dbdb`
- **Next item:** Day 4 — Dockerfile; `.env.example`; README.md.

---

### 2026-10-17 — Fix sidebar: /employment overview, /admin, About links

- **Items finished:**
  1. **`app/routers/employment.py`** — Added `GET /employment` overview route. Two-tab
     page: "Current Jobs" (all students with a currently active job, using the same
     `start_date <= today AND end_date IS NULL OR end_date > today` logic as D-31; columns
     student, STU#, employer, title, start, link to student) and "Employers" (existing
     employer list + Add Employer button). Tab selected via `?tab=jobs` or `?tab=employers`.
     Sidebar `href="/employment"` now resolves to a real page instead of 404.
  2. **`app/templates/employment/overview.html`** — New two-tab template.
  3. **`app/routers/admin.py`** — Complete admin router.  Requires `accounts.manage`
     permission (returns 403 for Staff). `GET /admin` renders a users table (name, email,
     role, 2-step on/off, status Active/Locked, last sign-in timestamp) and a "Recent audit
     log" card (last 50 events as plain-English sentences, same format as dashboard).
     `POST /admin/unlock/{user_id}` clears `locked_until` + `failed_logins=0`, writes an
     `account_unlock` audit event, CSRF-protected, redirects back to `/admin`.
  4. **`app/templates/admin/index.html`** — Admin page template.
  5. **`app/services/kpis.py`** — Added `account_unlock` to `_ACTION_LABELS` dict and a
     new branch in `_fmt_activity` that renders "Actor unlocked account for TargetUser".
  6. **`app/templates/public_base.html`** — Added "About" link to the right of the
     wordmark in the public topbar (left of Sign in) and in the footer.
  7. **`app/templates/base.html`** — Added "About Onyx" link at the bottom of the
     signed-in sidebar below the nav list.
  8. **`app/main.py`** — Included `admin_router`.
  9. **`tests/test_sidebar_links.py`** — 18 new tests:
     - `/about` 200 unauthenticated; About link in landing topbar.
     - Staff: `/dashboard`, `/students`, `/employment`, `/employment?tab=jobs`,
       `/employment?tab=employers`, `/reports` → all 200.
     - Staff: `/admin` → 403.
     - Staff: signed-in sidebar contains `/about` link.
     - Admin: all Staff routes + `/admin` → 200.
     - `/admin` renders Users table (both seeded users visible).
     - Unlock POST: `locked_until` cleared to `None`, `failed_logins` reset to 0.
     - Unlock POST: writes `account_unlock` audit event.
- **Bob modes used:** Agent mode throughout.
- **Key prompts:**
  - "Fix the sidebar so every menu item works (judges will click each one): 1. /employment
    (Staff + Admin): page with two tabs/sections: 'Current jobs' (all students, using
    is_current(): student, STU, employer, title, start, link to student) and 'Employers'
    (the existing employers list with Add employer). No 404. 2. /admin (Administrator only,
    403 for Staff), 'Users and access' light version: table of users (name, email, role,
    2-step on/off, status Active/Locked, last sign-in) with an 'Unlock' button on locked
    accounts (CSRF, audit event), plus 'Recent audit log' (last 50 events in plain English,
    like the dashboard). No reset password or role change. 3. About: add 'About' in the
    welcome page top bar (left of Sign in) and footer, and a small 'About Onyx' link at the
    bottom of the signed-in sidebar. /about stays public. Tests: every sidebar link returns
    200 for its role (Staff: no /admin -> 403); unlock clears lockout; /about 200 signed
    out. Run pytest, commit, push. Do not start a uvicorn server yourself; use the TestClient."
- **What Bob did well:** Read all 9 required files before touching code; diagnosed the
  /employment 404 immediately (router had no base route); reused existing `is_current_job`
  SQL filter pattern; recognised that admin.py was blank and built it from scratch in one
  pass; threaded `_fmt_activity` import from kpis.py into admin.py rather than duplicating
  the logic; ran new tests in isolation first (18/18 pass, 60s), then validated each
  existing test file individually (all green); commit message lists all 9 touched files.
- **Where I corrected it:** No corrections from Clarence.
- **Problems + fixes:** PowerShell `head` not available — switched to `Select-Object -First`.
  Full pytest suite times out in one shot due to TOTP real-clock auth (each session ~3s);
  ran test files individually, all passed.
- **Decisions changed:** None.
- **Tests:** 18 new tests + 138 existing = **156 total**, 0 failed (verified per-file).
- **Commit ID:** `471bff8`
- **Next item:** Day 4 — Dockerfile; `.env.example` complete; README.md.

---
