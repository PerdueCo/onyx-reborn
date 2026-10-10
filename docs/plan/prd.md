# PRD — How Onyx Reborn behaves (no code)

Screens reference the mockups in `docs/design-reference/design/mockups/`.

## Roles
| Role | Who | Can see / do |
|---|---|---|
| Admin | Program director / IT | Everything + Administration (users, roles, import, audit log) |
| Staff | Instructors, career services | Dashboard, Students, Employment, Reports |
| Reviewer (add-on role) | Selected staff | Approve/reject student update requests (only if portal requests are built) |
| Student | Enrolled students | My information, My employment (own record only). Only when `PORTAL_ENABLED` is on |

Roles are made of permissions (`students.read`, `students.manage`, `employment.manage`,
`reports.read`, `accounts.manage`, `student_updates.approve`, `self_service.use`), as defined in
`docs/design/DATABASE_SCHEMA.md`.

Any page a role isn't allowed to see returns a friendly "You don't have access" page (HTTP 403)
and is logged. Nav items a role can't use are hidden.

## 1. Landing page (replaces the splash screen) — mockup "student success welcome screen"
- Header: "Onyx Reborn" wordmark, **Sign in** button top-right.
- Hero: "A new chapter for student success" / "Student and employment management, modernized."
- Big **Sign in →** button. Footer: "Onyx Reborn — BSSI Modernization".
- Small "About this project" link → page with the 1998 → 2026 story and original authors
  (from the old `frmAbout`).

## 2. Sign in — mockup "account login screen"
- Email + password (eye icon toggles visibility). "Forgot password?" (shows "Contact your
  administrator" for MVP). "Back to welcome".
- Wrong email or password → one generic message: "Email or password is incorrect."
- 5 failed attempts in 15 min → account locked 15 min, shown as a message.
- No SSN anywhere.

## 3. MFA — mockup "MFA Verification Screen"
- **First sign-in:** user sees a QR code + text secret, scans it with Google/Microsoft
  Authenticator, enters the 6-digit code to confirm. Shown 8 one-time recovery codes once.
- **Every sign-in after:** "Verify your sign-in" with 6 boxes; auto-advances per digit.
- Wrong code → "That code didn't work. Try the newest code in your app."
- "Use a recovery code" link; each recovery code works once.
- Demo accounts have MFA pre-enrolled; their secrets are in the README for judges.

## 4. Layout after sign-in — mockups 13–17
- Navy left sidebar: Overview · Students · Employment · Reports · Administration (by role);
  students see Overview · My information · My employment.
- Top bar: search box (Staff/Admin: students by name or STU id), avatar with name + role,
  menu with **Sign out**.
- Sign out → back to landing page with "You've been signed out."
- Session expires after 30 min idle → sign-in page with "Your session timed out."

## 5. Dashboard / Overview (replaces the switchboard)
Admin/Staff see, uncluttered:
- **KPI cards (4):** Active students · Distinct students currently employed (%) · Current
  jobs (a job count, which can be higher than employed students) · Students seeking employment.
  Average hourly rate shows as a small line under the jobs card.
- **Chart 1:** Employed vs. seeking, by program (bar).
- **Chart 2:** Employer types (bar).
- **Recent activity:** last 8 changes (who, what, when) from the audit log.
- Each KPI card links to the matching filtered list or report ("details are in reports").
Students see a welcome card with their name, program, status, and current job.

## 6. Students (Staff/Admin)
- List: table with STU id, name, program, employed yes/no, seeking yes/no; search + filter by
  program; 25 per page.
- Student detail: profile card (mockup 13 layout), contact info, high school + grad date,
  job-seeking flag + desired job description, list of
  jobs (current and past).
- Add / Edit student form. Required: first name, last name, program, home phone.
  Phone format checked (`(555) 555-0101`). State is a dropdown. Save → success toast →
  detail page. Every save is written to the audit log.
- No SSN field. A student gets an auto ID `STU-0001`, `STU-0002`, …

## 7. Employment (Staff/Admin)
- Employers list: name, type, city, # students employed. Add/edit employer.
- On a student: **Add job** (employer, job title, supervisor, hours/week, hourly rate,
  start date, job type part/full-time). **End job** (end date). A student may hold
  more than one current job (mockup 13 shows 2).
- Hourly rate shown as `$17.25`. Hours 1–80.

## 8. Student self-service
- **My information:** own profile, read-only, with note "To correct your information, contact
  career services."
- **My employment:** own jobs, read-only.
- A student trying to open any other student's URL gets 403.
- (Stretch: "Submit employment update" → request → Staff review queue → approve/reject/needs
  correction, per mockups 14–17. Approved requests change the record; nothing auto-applies.)

## 9. Reports (Staff/Admin) — replaces the 5 print reports
1. **Student roster** (filter: program, employed, seeking).
2. **Current employment** (student, employer, title, hours, rate).
3. **Employer summary** (employer, type, # students, avg rate).
Each: on-screen table, **Export CSV**, **Print** (print-friendly CSS). Stretch: PDF.

## 10. Administration (Admin) — finishes the never-built "Student Maintenance"
- **Users:** list, create user (email, name, role, link to student record if Student),
  disable/enable, reset MFA.
- **Legacy import:** button "Import 1998 BSSI data" → runs the importer on the bundled test
  files → shows a result summary (rows read, imported, skipped, SSNs discarded = N).
  Safe to run twice (no duplicates).
- **Audit log:** table of who did what, when (sign-in, failed sign-in, create/edit/delete,
  import, access denied). Filter by user/action.

## Edge cases to handle
- Duplicate student (same first+last+home phone) → warn "A student with this name and phone
  already exists" with link, allow save anyway (mirrors the 1998 "already on file" prompt).
- Ending a job with an end date before the start date → blocked with message.
- Deleting is soft (record marked inactive) so history and audit remain.
- Empty states: "No students yet — import the 1998 data or add one."
