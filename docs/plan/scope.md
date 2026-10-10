# Scope — Onyx Reborn

## One-liner
Onyx Reborn turns a 1998 16-bit Visual Basic 4 student-and-employment tracker that wrote to
fixed-width flat files on a floppy drive into a secure, role-based, cloud-hosted web app —
with the original data migrated, SSN logins removed, and a modern dashboard in place of the
old switchboard.

## Origin story (use in the pitch)
BSSI was the capstone project of the Onyx group (Clarence Perdue Jr., Bela, Walter Hicks,
Jason Via, Costanza Baez) at Gwinnett Technical Institute, 1998. It tracked students in the
Business Science programs and where they worked. It no longer runs on modern Windows (16-bit
VB4), it stored data in fixed-width files on `A:\`, and it identified students by Social
Security Number. The full forensic read of the old code is in
`docs/analysis/legacy-inspection-report.md`.

## Hackathon fit
- **Track:** Theme 2 — Experienced Developers, "Modernize What Matters."
- **Judging:** Tool usage & depth of Bob adoption 30% · Innovation & relevance 30% ·
  Functionality & execution 30% · Presentation 10%.
- **What we must submit (by Oct 18):** GitHub repo (code, README, deploy files, test
  instructions) · ≤100-word description · track · tech stack · list of improvements ·
  PDF pitch deck · ≤3-min YouTube demo · live demo link.

## Legacy → modern map (the heart of the story)
| 1998 BSSI | 2026 Onyx Reborn |
|---|---|
| Splash screen (`SPLASH~1.FRM`) | Public landing page with "Sign in" |
| SSN typed twice to "log in" (`SSN.FRM`) | Email + password + authenticator-app MFA; SSN never collected |
| Switchboard / main menu (`MAINMENU.FRM`, `SWITCH.FRM`) | Dashboard with KPI cards + left nav |
| Fixed-width flat files on `A:\` / `E:\` | Relational database (SQLite → PostgreSQL) with a real schema |
| No roles (anyone at the PC sees everything) | Admin / Staff / Student roles, enforced on every page |
| Student & employment entry forms | Student and Employment pages (list, view, add, edit) |
| Print-to-form reports (`frmPrintSS`) | Reports page: filter, view, export CSV, print-friendly |
| Unfinished "Student Maintenance" / `frmInstructor` | Finished as the Administration area (users, roles, import, audit log) |
| Company code = 4 letters + 4 phone digits (collision-prone) | Real employer IDs; old code kept as `legacy_code` |
| Runs on one PC | Docker container on IBM Cloud |

## In scope (must ship — MVP)
1. Landing page → Sign in → MFA (TOTP) → role-based dashboard.
2. Roles: **Admin**, **Staff**, **Student**.
3. Dashboard (Admin/Staff): KPI cards, one or two simple charts, recent activity.
4. Students area (Staff/Admin): list, search, view, add, edit.
5. Employment area (Staff/Admin): employers + student job records, add/edit/end a job.
6. Student self-service (read-only "My information" / "My employment"). Optional, behind
   `PORTAL_ENABLED`, go/no-go at the Oct 11 checkpoint. Staff features never depend on it.
7. Reports: 3 reports, view + CSV export + print.
8. Administration: manage users and roles, run legacy import, view audit log.
9. Legacy importer: reads the original fixed-width `Student.txt` / `Employment.txt`
   into the database, drops SSNs, assigns `STU-xxxx` IDs.
10. Deployed live on the cloud with a demo account per role.

## Stretch (only if MVP is done by Thu Oct 15 night)
- Student "Submit employment update" requests + Staff review queue (mockups 14–17).
- PDF export of reports.
- Password reset by email.

## Out of scope
- Real student data, real email delivery, SSO/enterprise identity provider, mobile app,
  React rewrite (listed as roadmap in the deck).

## Required finish line (from DATABASE_SCHEMA.md §1)
Authorized staff can create, find, view and edit students, record two simultaneous jobs,
end one job without losing its history, and run a report.

## Success = demo script works end to end
Landing → sign in as Staff → MFA code → dashboard KPIs → find student → add a job →
report shows it → export CSV → sign in as Student → sees only own record →
sign in as Admin → shows import of the 1998 flat files + audit log.
