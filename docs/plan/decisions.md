# Decisions log

Answers to the 10 questions in `docs/analysis/legacy-inspection-report.md` §7, plus new ones.
**Status:** `PROPOSED` = Claude's default, Clarence to confirm · `CONFIRMED` = Clarence agreed.

| # | Question | Decision | Status |
|---|---|---|---|
| D-01 (Q1) | Production file paths A:\ vs E:\ | Irrelevant to the new app; importer reads the reporting copies from the repo test pack. Note in README that 1998 paths were hard-coded. | CONFIRMED |
| D-02 (Q2) | Instructor / Student Maintenance | Never finished in 1998. Finished now as the **Administration** area + Staff role. Great pitch line. | CONFIRMED |
| D-03 (Q3) | Company code collisions | Replace with real employer IDs; keep old code as `employers.legacy_code` only. | CONFIRMED |
| D-04 (Q4) | YesNo encoding 0/1 vs Y/N | Store as boolean `seeking_employment`; importer accepts both. | CONFIRMED |
| D-05 (Q5) | Student `Date` field (test data has e.g. `01/15/98`) | Import as `enrolled_date` (add column); blank → NULL. | CONFIRMED |
| D-06 (Q6) | Employer state never saved (bug) | Fixed — state is saved. List under "bugs fixed" in submission. | CONFIRMED |
| D-07 (Q7) | Hours/week 2 vs 3 digits | Integer 1–80. | CONFIRMED |
| D-08 (Q8) | One employer per student? | Many jobs per student (mockup 13 shows 2), with start/end dates for history. | CONFIRMED |
| D-09 (Q9) | Report output | On-screen + CSV + browser print; PDF is stretch. | CONFIRMED |
| D-10 (Q10) | Name | "Onyx Reborn — BSSI Modernization". Keep ONYX. | CONFIRMED |
| D-11 | Cloud DB | Start: SQLite re-seeded in container (demo). Upgrade to IBM Cloud PostgreSQL if time on Day 8. | CONFIRMED |
| D-12 | SSN | Never collected, stored, or displayed. Importer discards it. Student ID = `STU-####`. | CONFIRMED |
| D-13 | MFA method | TOTP authenticator app (pyotp) + 8 recovery codes. No SMS (cost, SIM-swap risk). Superseded by D-17/D-18. | CONFIRMED |
| D-14 | Year of original app | 1998 (VB4; dates in forms are April–May 1998). | CONFIRMED |
| D-15 | Student self-service editing | Read-only for MVP; request/review workflow is stretch. Superseded by D-24. | CONFIRMED |
| D-16 | Team | Solo — Clarence Perdue Jr. The 1998 Onyx group (Clarence Perdue Jr., Bela, Walter Hicks, Jason Via, Costanza Baez) credited as original authors only in the pitch deck. | CONFIRMED |

## Reconciliation with `docs/design/DATABASE_SCHEMA.md` (added Oct 9)
The schema doc wins wherever it disagrees with the plan. These decisions close the gaps
between the two.

| # | Question | Decision | Status |
|---|---|---|---|
| D-17 | Identity provider (schema §6 leaves it open) | **Local provider** for the hackathon: `user_account.provider='local'`, credentials + TOTP in a separate `local_credential` table so a real provider can replace it later. Free, works offline, demoable. Real provider = roadmap slide. *Replaces D-13's "no table" tension: there's no MFA-code table, only an encrypted secret.* | CONFIRMED |
| D-18 | MFA scope | Required for Administrator and Staff. Student MFA optional (enroll on first login if the portal is on). | CONFIRMED |
| D-19 | Student number format | `STU-####`, generated on create, immutable (mockups use STU-0104). | CONFIRMED |
| D-20 | Legacy fields to keep | Keep as optional: two phones, address, high school, grad date, seeking flag, desired job, enrolled date. **Drop birth month/day** — same treatment as SSN: discarded on import, never stored. | CONFIRMED |
| D-21 | Imported jobs have no start date, but the schema requires one | Use the student's legacy `enrolled_date` (e.g. 01/15/98) as start_date and note "start date inferred from 1998 entry date" in the import audit event. | CONFIRMED |
| D-22 | Imported job_type unknown | Allow `unknown` in addition to part_time/full_time/other; staff can fix it later. | CONFIRMED |
| D-23 | Roles & approver | Administrator: all permissions including `student_updates.approve`. Staff: `students.read`, `students.manage`, `employment.manage`, `reports.read`. Separate **Reviewer** role holds `student_updates.approve` only (assign to selected staff). Student: `self_service.use`. All three seeded on Day 1. | CONFIRMED |
| D-24 | Portal checkpoint | Schema says decide at the **Oct 11** checkpoint. Build is staff-first either way; the portal sits behind `PORTAL_ENABLED`. Read-only "My information/My employment" is cheap, so try it after staff core; the request/review queue only if Day 6 is finished by Thu Oct 15. | CONFIRMED |

## Oct 11 checkpoint decisions (D-27)

| # | Question | Decision | Status |
|---|---|---|---|
| D-27 | Oct 11 scope cut | **Staff-first confirmed.** Student portal (read-only self-service) = OUT for the hackathon; move to roadmap slide. Request/review queue = OUT. Admin user-management UI = OUT — demo users created by `scripts/seed.py`; no `/admin/users` page. Audit events still recorded to DB; no viewer page. Reports cut to **1 report + CSV** (Employment history by employer). These cuts leave 4 working days free to finish students, auth, employment, deploy, and the pitch deck. | CONFIRMED |
| D-25 | Migrations | Alembic from day 1 (schema §4 asks for explicit migrations). | CONFIRMED |
| D-26 | `UI_FLOW.md` | `prd.md` is the UI flow document. No separate `UI_FLOW.md` will be created. | CONFIRMED |

## Auth decisions (D-28 – D-30)

| # | Question | Decision | Status |
|---|---|---|---|
| D-28 | Overview MVP scope | Dashboard shows 4 KPI cards (placeholder `—` values until Day 5 employment data exists). No charts in MVP. Real DB counts wired when employment is built. | CONFIRMED |
| D-29 | Users and access light | Admin-only `/admin/users` page: list users, Unlock (clear `locked_until`), Reset password (set a temp password), Change role. No create-user UI for MVP; users created by `reset_db.py`. | CONFIRMED |
| D-30 | 2-step always required | TOTP MFA is always enforced for Admin and Staff; no `TOTP_REQUIRED` flag. Tests generate real TOTP codes via `pyotp.TOTP(secret).now()` from the seeded known secret — no bypass. Demo users created only when `DEMO_MODE=true` (via `reset_db.py`). | CONFIRMED |

| D-31 | Current-job definition for detail page and KPIs | `current = start_date <= today AND (end_date IS NULL OR end_date > today)`. Strict `>` on end_date (a job that ended today is history by end of day). Single `is_current_job(job, today)` helper in `kpis.py` used by both the KPI queries and the student detail router split. | CONFIRMED |

Amends: **D-13** → see D-17/D-18. **D-15** → see D-24. **D-08** confirmed by the schema
(multiple simultaneous jobs; same employer may repeat).
