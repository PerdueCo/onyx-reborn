# Technical Spec — Onyx Reborn

## 1. Stack
| Layer | Choice | Why |
|---|---|---|
| Web | FastAPI + Jinja2 templates | Server-rendered, simple, fast to demo; already chosen in the legacy report |
| DB access | SQLAlchemy 2.0 ORM | Same code runs on SQLite and PostgreSQL |
| DB | SQLite (`onyx.db`) locally; PostgreSQL in cloud via `DATABASE_URL` | Zero setup locally, real DB in cloud |
| Auth | passlib[bcrypt] password hashes; signed session cookie (Starlette `SessionMiddleware`); `pyotp` TOTP; `qrcode` for enrollment QR | Real two-factor without a paid provider |
| Charts | Chart.js 4 from CDN | Two small charts only |
| Tests | pytest + FastAPI `TestClient` | |
| Deploy | Dockerfile → IBM Cloud Code Engine (IBM judges will like it); fallback Render | |

## 2. Folder layout
```
app/
  main.py            # create app, mount static, include routers, session middleware
  config.py          # settings from env (.env)
  db.py              # engine, SessionLocal, Base
  models.py          # all tables (DATABASE_SCHEMA.md + §3)
  security.py        # hash/verify pw, TOTP, login_required, require_permission(...), owns_student(...)
  audit.py           # log_event(db, user, action, entity, detail)
  routers/
    public.py        # landing, about
    auth.py          # login, mfa setup, mfa verify, logout
    dashboard.py
    students.py
    employment.py
    me.py            # student self-service
    reports.py
    admin.py
  services/
    kpis.py          # dashboard numbers
    legacy_import.py # fixed-width parser + loader (§5)
  templates/         # base.html (sidebar layout), public_base.html, one folder per router
  static/css/onyx.css, static/img/
migrations/          # Alembic
scripts/seed.py      # demo users + runs legacy import
tests/
Dockerfile, requirements.txt, .env.example, README.md
```

## 3. Database schema
**Source of truth: `docs/design/DATABASE_SCHEMA.md` (Clarence, Oct 8).** Follow its tables,
conventions (§4), integrity rules (§7) and acceptance checks (§8). This section only lists
how that schema is reconciled with the verified 1998 fields; each item is a decision in
`decisions.md` (D-17 to D-24) for Clarence to confirm.

Tables (from DATABASE_SCHEMA.md): `user_account`, `role`, `user_role`, `permission`,
`role_permission`, `program`, `student`, `employer`, `employment`, `change_request`
(optional portal), `audit_event`. Use Alembic migrations, not `create_all`. Turn on
`PRAGMA foreign_keys=ON` for every SQLite connection.

Additions that bring over the 1998 fields (all **optional/nullable**, none required):
```
student   + student_number 'STU-####' (D-19)
          + home_phone, work_phone            -- schema's single `phone` → keep 2, legacy-verified
          + address, city, state, zip, high_school, date_graduated
          + seeking_employment BOOL, desired_job TEXT     -- legacy YesNo + Description
          + enrolled_date DATE                            -- legacy Date (D-05)
          + legacy_source BOOL
          (birth month/day NOT carried over: data minimization, D-20)
employer  + address, city, state, zip, phone, company_type,
          + legacy_code  -- old 8-char Company_Code, traceability only (D-03)
employment+ supervisor, hourly_rate NUMERIC(8,2)          -- legacy Current_Supervisor, Amount
          job_type adds 'unknown' for imported rows (D-22)
local_credential  (new, only if D-17 = local provider)
          user_account_id PK/FK, password_hash, totp_secret_encrypted NULL,
          mfa_enabled BOOL, recovery_codes_hash JSON, failed_logins INT,
          locked_until NULL, updated_at
```
Imported jobs have no 1998 start date, but the schema requires one, so the importer uses the
student's `enrolled_date` and flags it with the audit event (D-21).
Current job = `start_date <= as_of AND (end_date IS NULL OR end_date >= as_of)`. KPIs and
reports always say whether they count **jobs** or **distinct students**.

## 4. Auth flow (depends on D-17)
Welcome → Login → MFA → role-appropriate dashboard. Once signed in, permissions come from
`role_permission` (e.g. `students.manage`), not role names. Routes check
`require_permission("students.manage")`. Student routes also check ownership.

**If D-17 = local provider (recommended for the hackathon):** `user_account.provider =
'local'`, `provider_subject` = a random UUID. Credentials and TOTP live in
`local_credential`, kept apart from identity, so a real provider (IBM Security Verify,
Auth0, Entra) can replace it later without touching `user_account`.
1. `POST /login` → active check, lockout (5 fails / 15 min), bcrypt verify → session
   `{uid, mfa_ok: false}`.
2. First time: `/mfa/setup` (pyotp QR, confirm code, 8 recovery codes shown once). After:
   `/mfa/verify` (`valid_window=1`) → `mfa_ok: true`.
3. TOTP secret encrypted at rest with `MFA_ENC_KEY` (Fernet). Never logged.
4. `SESSION_SECRET` from env; cookie `httponly`, `samesite=lax`, `secure` in cloud. CSRF
   token on every POST form.

**If D-17 = external provider:** follow DATABASE_SCHEMA.md §6. There is no `local_credential`
table, and MFA is configured at the provider.

## 4b. Student portal switch
`PORTAL_ENABLED=true|false` in env. When false, portal routes return 404 and their nav items,
plus any pending-request KPIs, disappear. Staff features must keep working (schema
§1, acceptance check 9).

## 5. Legacy importer (`services/legacy_import.py`)
Reads the **reporting copies** `Student.txt` (357-byte records, no line breaks) and
`Employment.txt` (238-byte records) from `docs/legacy-reference/legacy-code-copy/Data/`
(read-only; never written).

Student record slices (from `MAIN.BAS` `Student_File`):
`Program_Code 7 | Date 9 | Program_Name 31 | SS_Number 10 | Last_Name 16 | First_Name 16 |
Home_Phone 16 | Work_Phone 16 | Address 31 | City 31 | State 3 | zip 11 | High_School 31 |
Date_Graduated 11 | Month 3 | Day 3 | YesNo 2 | Description 101 | Company_Code 9` = 357

Employment record slices (`Employment_Type`):
`Company_Code 9 | Company_Name 31 | Address 26 | City 31 | State 3 | zip 11 | Job_Title 31 |
Current_Supervisor 31 | Phone_Number 16 | Hours_per_Week 3 | Amount 16 | Company_Type 30` = 238

Rules:
- Define field widths once as a list of `(name, width)`; assert they sum to 357 / 238.
- Read file as bytes, decode `cp1252`, chunk by record length, `.strip()` each field.
- **SS_Number is read and immediately discarded** — never stored, never logged. Count it.
- `YesNo`: test data uses `Y/N`; source code writes `0/1`. Accept `Y`,`1` → True; `N`,`0` → False.
- `Date_Graduated` `MM/DD/YYYY` → date; legacy `Date` `MM/DD/YY` → `enrolled_date`; `Month`/`Day` (birthday) are **discarded** like SSN (D-20); blanks → NULL.
- Employment `start_date` = student's `enrolled_date` (D-21); `job_type='unknown'` (D-22).
- `Amount` → Decimal, strip `$` and commas. Program code/name → upsert `programs`.
- Employer matched by `legacy_code`; student linked to employer via `Company_Code` → one
  `employment` row (end_date NULL).
- Idempotent: skip a student if (first, last, home_phone) already exists with `legacy_source`.
- Returns a summary dict; Admin page and `scripts/seed.py` both call it.
- Tests: field widths sum correctly; 5 students + 5 employers imported from test pack; running
  twice adds nothing; no SSN digits appear anywhere in the DB dump.

## 6. KPIs (`services/kpis.py`)
- total_students = active students
- employed = students with ≥1 employment where end_date IS NULL; pct = employed/total
- avg_hourly_rate = mean of current employments' hourly_rate
- seeking = students where seeking_employment = True

## 7. Config (`.env.example`)
```
DATABASE_URL=sqlite:///./onyx.db
SESSION_SECRET=change-me
ENV=dev
DEMO_MODE=true   # shows demo-account hint on login page
PORTAL_ENABLED=true
MFA_ENC_KEY=     # Fernet key for TOTP secrets
```

## 8. Deploy
- `Dockerfile`: python:3.12-slim, `pip install -r requirements.txt`,
  `CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}`.
- IBM Cloud Code Engine: build from GitHub repo, set env vars, PostgreSQL via IBM Cloud
  Databases for PostgreSQL **or** (simpler/free) keep SQLite inside the container and re-seed
  on startup when `DEMO_MODE=true`. Decide on Day 8; see decisions.md D-11.
- Fallback: Render web service from the Dockerfile.

## 9. Testing
`pytest -q` covers: importer, login/lockout, MFA verify, role access matrix (every route ×
every role → expected 200/302/403), student CRUD, KPIs, CSV export headers.
