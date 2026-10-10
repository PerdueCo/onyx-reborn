# Build checklist — Onyx Reborn

Bob: do ONE unchecked item at a time, run `pytest -q`, check it off, then stop and tell
Clarence how to see it. Mode hint in brackets: **[Ask]** understand · **[Plan]** design ·
**[Code]** build.

**Cut line:** if Day 6 isn't done by end of Thu Oct 15, skip all ⭐ stretch items.

## Day 0 — Fri Oct 9 / Sat Oct 10 morning: Get organized
- [ ] Commit what exists: `docs/`, `.gitignore`, these plan files, `AGENTS.md`, and `docs/design/DATABASE_SCHEMA.md`. Push.
- [ ] [Ask] Run the reconciliation prompt from `DATABASE_SCHEMA.md` §10, then confirm D-17 to D-26 in `decisions.md`
- [ ] [Ask] Bob reads `AGENTS.md` + plan docs and asks Clarence any gap questions → update `decisions.md` (mark CONFIRMED)
- [ ] Delete duplicate mockups (`-1`, `-3` copies are identical files)
- [ ] Create `docs/bob-log.md` and log this session

## Day 1 — Sat Oct 10: Skeleton + database
- [ ] [Plan→Code] Project skeleton per spec §2; `requirements.txt`; `uvicorn app.main:app --reload` shows "Onyx Reborn" at `/`
- [ ] [Code] `models.py` per DATABASE_SCHEMA.md + spec §3 additions; Alembic initial migration; SQLite FK pragma; seed roles + permissions (D-23)
- [ ] [Code] Schema tests for acceptance checks 1–4 (STU number immutable, 2 simultaneous jobs, end job keeps history, bad dates/negative hours/orphans rejected)
- [ ] [Code] `base.html` sidebar layout + `onyx.css` matching mockups
- [ ] [Code] pytest set up with in-memory SQLite fixture; 1 smoke test passes

## Day 2 — Sun Oct 11: Legacy importer (the modernization proof)
- [ ] [Ask] Bob explains the fixed-width layout back to Clarence from `MAIN.BAS`
- [ ] [Code] `legacy_import.py` per spec §5 + tests (widths, 5+5 rows, idempotent, no SSN or birth date in DB, start_date inferred per D-21)
- [ ] **Oct 11 checkpoint (D-24):** staff core on track? Decide portal go/no-go and record it
- [ ] [Code] `scripts/seed.py`: runs import + creates 3 demo users (admin/staff/student linked to an imported student)

## Day 3 — Mon Oct 12: Landing + sign in
- [ ] [Code] Landing page + About page (PRD §1)
- [ ] [Code] Login, logout, password hashing, lockout after 5 fails, generic error (PRD §2)
- [ ] [Code] Session timeout 30 min; CSRF token on forms
- [ ] Tests: login ok / wrong password / lockout

## Day 4 — Tue Oct 13: MFA + roles
- [ ] [Code] MFA setup (QR + recovery codes) and verify screens (PRD §3), using `local_credential` with the secret encrypted (D-17/D-18)
- [ ] [Code] `require_permission` dependency + ownership check; sidebar items by permission; 403 page
- [ ] [Code] Access matrix test (every route × role) = acceptance check 6
- [ ] Audit log writes for sign-in, failed sign-in, access denied

## Day 5 — Wed Oct 14: Dashboard + Students
- [ ] [Code] `kpis.py` + Overview page: 4 KPI cards, 2 Chart.js charts, recent activity (PRD §5)
- [ ] [Code] Students list/search/filter/paginate (PRD §6)
- [ ] [Code] Student detail + add/edit + duplicate warning + audit

## Day 6 — Thu Oct 15: Employment + self-service
- [ ] [Code] Employers list/add/edit (PRD §7)
- [ ] [Code] Add job / end job on student; validation
- [ ] [Code] Student "My information" / "My employment" + 403 on others (PRD §8), behind `PORTAL_ENABLED`; test that staff flows work with it off (check 9)

## Day 7 — Fri Oct 16: Reports + Admin
- [ ] [Code] 3 reports with filters, CSV export, print CSS (PRD §9)
- [ ] [Code] Admin: users (create/disable/reset MFA), Import button with summary, audit log viewer (PRD §10)
- [ ] ⭐ Change requests + Reviewer queue (mockups 14–17), with version-checked atomic approval (DATABASE_SCHEMA.md checks 7–8)

## Day 8 — Sat Oct 17: Ship it
- [ ] [Code] Dockerfile; runs locally with `docker run`
- [ ] Deploy to IBM Cloud Code Engine (fallback Render); demo accounts work live
- [ ] [Code] README: what it is, 1998→2026 table, run locally, run tests, demo logins + MFA secrets, deploy steps, "Built with Bob" section
- [ ] Full demo-script run-through on the live URL (scope.md "Success"); fix bugs
- [ ] ⭐ PDF export · ⭐ PostgreSQL

## Day 9 — Sun Oct 18: Submit (target 6 PM ET, hard stop 11:59 PM)
- [ ] Record ≤3-min demo video → YouTube (unlisted is fine unless rules say otherwise)
- [ ] Pitch deck PDF: team, problem (1998 app), before/after, how Bob was used, demo screens, roadmap
- [ ] Write ≤100-word description, track = Theme 2, tech stack, improvements list (from `bob-log.md` + decisions D-03/D-06/D-08/D-12)
- [ ] Submit on AngelHack; double-check repo is public / shared
