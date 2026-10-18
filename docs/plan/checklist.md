# Build checklist — Onyx Reborn (5-day sprint)

Bob: do ONE unchecked item at a time, run `pytest -q`, check it off, then stop and tell
Clarence how to see it. Mode hint in brackets: **[Ask]** understand · **[Plan]** design ·
**[Code]** build.

Scope cuts recorded in `decisions.md` D-27 (Oct 11 checkpoint).

---

## ✅ Already done (Days 0–2 equivalent)

- [x] Commit plan docs, schema, legacy analysis, mockups (commit `b8f93aa`)
- [x] Confirm all decisions D-01 – D-26 in `decisions.md`
- [x] Project skeleton: FastAPI + Jinja2 + SQLAlchemy + Alembic; pytest green (commit `97b1eab`)
- [x] `models.py` — all 12 ORM tables; Alembic initial migration; FK pragma; seed roles (commit `66d2007`)
- [x] `base.html` sidebar layout; `onyx.css` design tokens; `/dashboard` placeholder; 10 tests (commit `1dfbf7b`)
- [x] Welcome page: two-column grid, illustration PNGs, Inter font, exact type + spacing; 11 tests (commits `fb560dc`, `b4d2d49`)
  - ⚠️ **Day 5 polish leftovers:** desktop headline should break on exactly 2 lines ("A new chapter for / student success") — needs `<br>` confirmed at 1440 px; footer left-align verified at desktop.

---

## Day 1 — Mon Oct 13: Students + 1998 importer (~4 hrs)

- [x] [Code] Students list + search (name or STU number), add form, edit form; STU number `STU-####` generated and immutable; required-field validation; tests (acceptance checks 1 and 4) (commit `acb986e`, fixed commit `9fbd79c`)
- [x] [Code] `app/services/legacy_import.py` — fixed-width parser per spec §5; drops SSN + birth data; `start_date` inferred from enrolled_date (D-21); idempotent on re-run; tests (widths, 5+5 rows, no SSN in DB)
- [x] [Code] `scripts/seed_demo.py` — ~250 fictional students, ~12 employers, ~183 jobs (17 dual-current, ~40 seeking); idempotent; never touches legacy rows
- [x] [Code] `scripts/reset_db.py` — drop → migrate → seed roles → import 1998 → seed demo → two demo users; prints credentials
- [x] [Ask] Bob explains the fixed-width record layout from `MAIN.BAS` back to Clarence before coding the importer

---

## Day 2 — Tue Oct 14: Sign-in + 2-step TOTP + roles (~4 hrs)

- [x] [Code] Login, logout, password hashing (bcrypt), lockout after 5 fails, generic error message (PRD §2) (commit `acb986e`)
- [x] [Code] Session cookie (30-min timeout); CSRF token on all POST forms (commit `acb986e`)
- [x] [Code] TOTP 2-step verify screen (pyotp); MFA setup flow (QR code + 8 recovery codes) using `local_credential` (D-17/D-18) (commit `acb986e`)
- [x] [Code] `require_permission` FastAPI dependency; sidebar items filtered by role; 403 page (commit `ae750f7`)
- [x] [Code] Audit log writes: sign-in ok, sign-in failed, access denied (commit `acb986e`)
- [x] Tests: login ok / wrong password / lockout / TOTP correct / TOTP wrong (14 tests — commits `0e7781e`, `e6095f0`, 25 passed total)

---

## Day 3 — Wed Oct 15: Employment + employers + dashboard real numbers (~4 hrs)

- [x] [Code] Employers list + add + edit (name, address, city, state, phone — D-06 bug fixed)
- [x] [Code] Add job / end job on student detail page; start/end date validation; `job_type` dropdown
- [ ] [Code] `app/services/kpis.py` — real counts: total students, active jobs, employers, students seeking work
- [ ] [Code] Dashboard Overview: 4 KPI cards wired to real DB counts; recent activity feed (last 10 audit events); no Chart.js (cut — too slow to build well)
- [ ] Tests: add employer, add job, end job, overlapping-date guard

---

## Day 4 — Thu Oct 16: 1 report + CSV + deploy + README (~4 hrs)

- [ ] [Code] Employment history report: filter by employer and/or date range; paginated HTML table; CSV download button; `reports.read` permission guard (PRD §9, cut to 1 report per D-27)
- [ ] [Code] `Dockerfile`; `.env.example` complete; `docker run` shows the app locally
- [ ] Deploy to IBM Cloud Code Engine (fallback: Render free tier); demo accounts work on the live URL
- [ ] [Code] `README.md`: what it is, 1998 → 2026 comparison table, run locally, run tests, demo logins + TOTP secrets, deploy steps, "Built with Bob" section

---

## Day 5 — Fri Oct 17: Polish + demo video + pitch deck + submit (~4 hrs)

- [ ] Polish leftovers: confirm desktop headline 2-line break at 1440 px; confirm footer left-aligned; fix any visual regressions found during demo run-through
- [ ] (Optional) 2× retina welcome illustration — see `docs/plan/welcome-page-next-steps.md` Step B
- [ ] Full demo-script run-through on the live URL (`scope.md` "Success"); fix any bugs
- [ ] Record ≤3-min demo video → YouTube (unlisted)
- [ ] Pitch deck PDF: team, problem (1998 app), before/after screenshots, how Bob was used, demo screens, roadmap (portal, admin UI, review queue, PostgreSQL, PDF export)
- [ ] Write ≤100-word submission description; track = Theme 2; tech stack; improvements list (D-03/D-06/D-08/D-12)
- [ ] Submit on AngelHack by 6 PM ET; verify repo is public / shared

---

## Roadmap (after hackathon — cut from sprint per D-27)

- Student portal: read-only "My information" / "My employment" behind `PORTAL_ENABLED`
- Request/review queue with version-checked atomic approval (`ChangeRequest` model already in DB)
- Admin user-management UI (`/admin/users` create/disable/reset MFA)
- Audit log viewer page
- 2nd and 3rd reports (students by program; students seeking work)
- PDF export (print CSS already in plan)
- PostgreSQL upgrade (Alembic + `render_as_batch` already wired)
- Real identity provider (SAML/OIDC) — `user_account.provider` column already in schema
