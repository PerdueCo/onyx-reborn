# Auth Plan — Sign-in, MFA, Sessions, Permissions

**Scope:** spec.md §4 · decisions.md D-17/D-18/D-23 · prd.md §2–4  
**Goal:** Replace the DEV MODE stub with real local-provider authentication, TOTP MFA,
role-gated routes, a seeded `reset_db.py` that prints demo credentials, and a 403 page.  
**Non-goals:** External identity providers (roadmap), student self-service (portal gate).

---

## Sub-task 1 — Expand `app/security.py`

**Status:** [ ] pending

**Intent**  
Add all auth helpers to the one module spec.md designates: TOTP generate/verify,
Fernet encryption of the TOTP secret, CSRF token generation/verification,
`get_current_user()` FastAPI dependency (reads session → returns UserAccount or None),
and `require_permission(code)` dependency factory (raises 403 if the user lacks the
permission or is not signed in).

**Expected Outcomes**
- `hash_password` / `verify_password` already present — keep them.
- `encrypt_totp_secret(plain: str) -> str` and `decrypt_totp_secret(enc: str) -> str`
  using Fernet with `MFA_ENC_KEY` from settings.
- `generate_totp_secret() -> str` via `pyotp.random_base32()`.
- `totp_now(secret: str) -> str` and `verify_totp(secret, code, valid_window=1) -> bool`.
- `generate_recovery_codes() -> tuple[list[str], list[str]]` — returns (plaintext x8,
  bcrypt_hashes x8).
- `verify_recovery_code(plain: str, hashes: list[str]) -> int | None` — returns the
  index of the matching hash so the caller can remove it, or None.
- `csrf_token(request) -> str` — reads or generates `request.session["csrf"]`.
- `check_csrf(request, token_from_form)` — raises 403 on mismatch.
- `get_current_user(request, db) -> UserAccount | None` — reads `session["uid"]`,
  loads the UserAccount row, returns None if missing or inactive.
- `require_permission(code: str)` — dependency factory; calls `get_current_user`;
  if None → redirect to `/login?next=...`; if lacks permission → raises HTTP 403.

**Todo List**
1. Import `Fernet` from `cryptography.fernet`, `pyotp`, `bcrypt`, `secrets`, `hashlib`.
2. Add Fernet helpers (encrypt/decrypt). Guard: if `MFA_ENC_KEY` is empty, raise a
   clear `RuntimeError` so it is never silently skipped in production.
3. Add TOTP helpers wrapping `pyotp`.
4. Add recovery-code helpers (generate 8 × 10-char alphanumeric plaintext codes;
   hash each with bcrypt).
5. Add CSRF helpers using `request.session`.
6. Add `get_current_user` reading `session["uid"]` + DB lookup.
7. Add `require_permission` factory.

**Relevant Context**
- `app/security.py` — extend, do not replace.
- `app/config.py` — `MFA_ENC_KEY: str` already present.
- `app/models.py` — `UserAccount`, `LocalCredential`, `UserRole`, `RolePermission`, `Permission`.
- `app/db.py` — `get_db` dependency.
- spec.md §4: "TOTP secret encrypted at rest with `MFA_ENC_KEY` (Fernet). Never logged."

---

## Sub-task 2 — Implement `app/audit.py`

**Status:** [ ] pending

**Intent**  
Replace the placeholder `log_event` with a real writer that inserts an `AuditEvent` row.
Must not raise; uses a best-effort pattern (commit failure is silently swallowed so auth
flows never break because an audit write failed).

**Expected Outcomes**
- `log_event(db, user_id, action, entity_type, entity_id, detail)` inserts and commits
  an `AuditEvent` row.
- Called from `auth.py` for: `sign_in_ok`, `sign_in_failed`, `sign_in_locked`,
  `sign_out`, `mfa_setup`, `mfa_ok`.
- Called from `students.py` for: `student_create`, `student_edit` (already stubbed).

**Todo List**
1. Import `AuditEvent` from `app.models`.
2. Replace the `pass` body with an `AuditEvent(...)` insert + `db.commit()` wrapped in
   `try/except Exception`.

**Relevant Context**
- `app/audit.py` — current placeholder.
- `app/models.py` — `AuditEvent` columns: `actor_account_id`, `event_type`,
  `entity_type`, `entity_id`, `occurred_at`, `detail`.

---

## Sub-task 3 — Build `app/routers/auth.py`

**Status:** [ ] pending

**Intent**  
Implement the full local-provider auth flow: login form → password check → lockout →
MFA setup (first sign-in) → MFA verify → session issue → logout.

**Expected Outcomes**

| Route | Method | Purpose |
|---|---|---|
| `/login` | GET | Show email+password form; CSRF token in hidden field |
| `/login` | POST | Verify credentials; set `session["uid"]`; redirect to MFA |
| `/mfa/setup` | GET | Show QR code + text secret (first-time only) |
| `/mfa/setup` | POST | Verify first code; store encrypted secret; show 8 recovery codes once |
| `/mfa/verify` | GET | Show 6-digit input |
| `/mfa/verify` | POST | Verify TOTP; set `session["mfa_ok"]=True`; redirect to `/dashboard` |
| `/logout` | POST | Clear session; redirect to `/` with flash "You've been signed out." |

**Rules per spec.md §4 / prd.md §2–3:**
- Wrong email or password → "Email or password is incorrect." (no distinction).
- 5 failed attempts within a rolling 15-min window → `locked_until = now + 15 min`;
  message: "Account locked. Try again in 15 minutes."
- Session cookie: `session["uid"]` set after password check; `session["mfa_ok"]` set
  only after TOTP passes. Protected routes check **both**.
- 30-min idle timeout: set `session["last_active"]` on every authenticated request;
  `get_current_user` checks it and clears the session if stale.
- CSRF: every POST form includes `<input name="csrf_token" value="{{ csrf_token }}">`;
  handler calls `check_csrf(request, token)`.
- `TOTP_REQUIRED` env flag: when False, skip MFA and set `mfa_ok=True` immediately
  (useful for automated tests without a live TOTP device).
- `DEMO_MODE=true` in settings: show "Demo accounts" hint below the login form.

**Todo List**
1. Scaffold `auth.py` router; import security helpers, audit, get_db.
2. `GET /login` — render `auth/login.html` with CSRF token; redirect to `/dashboard` if
   already fully signed in.
3. `POST /login` — load user by email (via `LocalCredential.provider_subject` lookup or
   `UserAccount.email`). Check active, lockout window, bcrypt. On success set
   `session["uid"]`; reset `failed_logins`. On fail increment `failed_logins`; check
   threshold; log audit event. Redirect to `/mfa/setup` if not enrolled, `/mfa/verify`
   otherwise (or `/dashboard` if TOTP_REQUIRED=false).
4. `GET /mfa/setup` — generate secret, store **unencrypted** in session temporarily;
   render QR code as base64 PNG via `qrcode`; show text secret.
5. `POST /mfa/setup` — verify code against session secret; encrypt and save to
   `LocalCredential`; generate 8 recovery codes; render one-time display page.
6. `GET /mfa/verify` — render `auth/mfa_verify.html`; redirect if already `mfa_ok`.
7. `POST /mfa/verify` — try TOTP first, then recovery codes; on success set
   `session["mfa_ok"]=True`; log `mfa_ok`; redirect to `next` param or `/dashboard`.
8. `POST /logout` — clear session; log `sign_out`; redirect to `/`.

**Relevant Context**
- `app/security.py` (sub-task 1 output).
- `app/models.py` — `LocalCredential.locked_until`, `failed_logins`, `mfa_enabled`.
- `spec.md §4` — session shape, CSRF, lockout numbers.
- `app/templates/auth/` — three new templates (login, mfa_setup, mfa_verify).

---

## Sub-task 4 — Templates: `auth/login.html`, `auth/mfa_setup.html`, `auth/mfa_verify.html`

**Status:** [ ] pending

**Intent**  
Server-rendered forms matching the mockup style (white card, centered, public_base.html).

**Expected Outcomes**
- `auth/login.html`: email input, password input with eye-toggle (JS), CSRF hidden field,
  "Sign in" primary button, error message div, "Forgot password?" note
  ("Contact your administrator"), "Back to welcome" link.
  If `DEMO_MODE`: grey hint block listing demo logins.
- `auth/mfa_setup.html`: QR code `<img>`, text secret, single 6-digit code input, submit.
  Recovery codes shown on a separate `auth/mfa_recovery.html` page — display once.
- `auth/mfa_verify.html`: "Verify your sign-in" heading, 6 individual digit inputs
  (auto-advance via small inline JS), "Use a recovery code" link, error message.

**Todo List**
1. Create `app/templates/auth/` directory.
2. Write `login.html` extending `public_base.html`.
3. Write `mfa_setup.html` extending `public_base.html`.
4. Write `mfa_recovery.html` (one-time display) extending `public_base.html`.
5. Write `mfa_verify.html` extending `public_base.html`.

**Relevant Context**
- `app/templates/public_base.html` — parent template, dark topbar.
- Mockups: `docs/design-reference/design/mockups/Onyx Reborn account login screen.png`
  and `…MFA Verification Screen.png` (deleted from git index but the filenames are
  referenced in prd.md; design intent is white card, centered, `public_base.html`).

---

## Sub-task 5 — Gate staff routes + 403 page + remove DEV MODE

**Status:** [ ] pending

**Intent**  
Add `require_permission` to every staff route, filter the sidebar by the current user's
permissions, render a friendly 403 page, and remove the DEV MODE amber banner from
`base.html` (authentication is real now).

**Expected Outcomes**
- `GET /dashboard` — requires `students.read` (any logged-in Staff or Admin).
- `GET /students*` — requires `students.read`; write actions require `students.manage`.
- `GET /admin*` — requires `accounts.manage` (Admin only).
- `base.html` sidebar: navigation items hidden when the user lacks the required permission.
  Pass `user_perms: set[str]` from every authenticated route context.
- `app/templates/403.html` — friendly "You don't have access" page in the sidebar layout.
- `app/main.py` — register a custom 403 exception handler.
- DEV MODE amber banner **removed** from `base.html` (the "Not signed in" topbar state
  can remain as a passive indicator — do not add a new banner).
- `test_smoke.py` — update `test_dashboard_ok` to no longer assert `"DEV MODE"`.

**Todo List**
1. Import `require_permission` into `students.py` and `dashboard.py`; add as dependency.
2. Create `app/templates/403.html`.
3. Register 403 handler in `main.py`.
4. Update `base.html`: remove the `{% if not current_user %} dev-banner` block; add
   `{% if 'students.read' in user_perms %}` guards around nav items.
5. Update `test_smoke.py` `test_dashboard_ok` — remove DEV MODE assertion; dashboard now
   redirects to `/login` when unauthenticated (expect 302 or update the test to sign in).

**Relevant Context**
- `app/templates/base.html` — lines 93–100 are the DEV MODE banner to remove.
- `app/routers/dashboard.py` — currently passes `current_user=None`.
- `app/routers/students.py` — all handlers need the dependency.

---

## Sub-task 6 — `scripts/reset_db.py` (demo seeder)

**Status:** [ ] pending

**Intent**  
A single script that drops and recreates the DB, seeds roles/permissions, creates two demo
users with pre-enrolled TOTP, and **prints** the credentials so judges can log in.

**Expected Outcomes**
- Drops all tables; runs `Base.metadata.create_all`; seeds roles + permissions.
- Creates `admin@onyx.demo` (Administrator) and `staff@onyx.demo` (Staff), each with:
  - Known password (hardcoded constant, printed to stdout).
  - Known TOTP secret (hardcoded constant, encrypted and stored; printed to stdout).
  - `mfa_enabled = True`, `failed_logins = 0`.
- Prints a formatted block:

  ```
  ─── Onyx Reborn demo accounts ───────────────────────────
  admin@onyx.demo  password: OnyxAdmin2026!
    TOTP secret: BASE32SECRETHERE  (use in any authenticator app)
  staff@onyx.demo  password: OnyxStaff2026!
    TOTP secret: BASE32SECRETHERE
  ─────────────────────────────────────────────────────────
  ```
- Idempotent only in the sense that re-running it **wipes and re-seeds** (intended for demo
  reset, not incremental migration — the script is named `reset_db.py` accordingly).
- Seeds the 5 programs (CIS101, ACC110, BUS201, MKT130, OFT120).

**Todo List**
1. Create `scripts/reset_db.py`.
2. Import `Base`, engine, `seed` from `seed_roles`, models.
3. `Base.metadata.drop_all(engine)` → `Base.metadata.create_all(engine)`.
4. Call `seed_roles.seed(session)`.
5. Create two `UserAccount` rows + two `LocalCredential` rows (bcrypt pw, encrypted TOTP).
6. Print the credentials block.
7. Seed programs.

**Relevant Context**
- `scripts/seed_roles.py` — reuse `seed()`.
- `app/security.py` — `hash_password`, `encrypt_totp_secret`.
- `app/models.py` — `UserAccount`, `LocalCredential`, `UserRole`.

---

## Sub-task 7 — Tests: `tests/test_auth.py`

**Status:** [ ] pending

**Intent**  
Cover the auth acceptance checks from spec.md §9.

**Expected Outcomes**
Tests (all use `db_session` fixture + `TestClient`):

| Test | What it checks |
|---|---|
| `test_login_ok` | POST /login with correct credentials → 302 to /mfa/verify |
| `test_login_wrong_password` | wrong password → 200 with error message, no session uid |
| `test_login_lockout` | 5 bad attempts → response contains "locked" |
| `test_login_locked_account` | 6th attempt while locked → still locked message |
| `test_totp_correct` | correct TOTP → session mfa_ok=True, redirect to /dashboard |
| `test_totp_wrong` | wrong code → 200 with error, no mfa_ok |
| `test_recovery_code_works` | valid recovery code → mfa_ok, code removed from list |
| `test_logout` | POST /logout → session cleared, redirect to / |
| `test_require_permission_redirect` | unauthenticated GET /students → 302 to /login |
| `test_403_wrong_role` | student role account → GET /students → 403 |

**Todo List**
1. Create `tests/test_auth.py`.
2. Add a `seeded_db` pytest fixture (or extend `db_session`) that creates the two demo
   users with known passwords and TOTP secrets.
3. Write each test above using `TestClient` with session override or direct DB seeding.

**Relevant Context**
- `tests/conftest.py` — `db_session` and `client` fixtures.
- `app/security.py` — helpers to seed LocalCredential rows in tests.
- FastAPI `TestClient` docs — cookie-based session state between requests.

---

## Open Questions / Decisions Needed Before Implementation

None — all decisions are already confirmed (D-17 local provider, D-18 MFA required for
Admin/Staff, D-23 roles). The `TOTP_REQUIRED` env flag is a new addition not yet in
decisions.md; it will be recorded as **D-28** when Clarence approves this plan.

---

## Files Changed

| File | Action |
|---|---|
| `app/security.py` | Extend (sub-task 1) |
| `app/audit.py` | Replace placeholder (sub-task 2) |
| `app/routers/auth.py` | Create (sub-task 3) |
| `app/templates/auth/login.html` | Create (sub-task 4) |
| `app/templates/auth/mfa_setup.html` | Create (sub-task 4) |
| `app/templates/auth/mfa_recovery.html` | Create (sub-task 4) |
| `app/templates/auth/mfa_verify.html` | Create (sub-task 4) |
| `app/templates/403.html` | Create (sub-task 5) |
| `app/templates/base.html` | Edit — remove DEV MODE banner, add permission guards (sub-task 5) |
| `app/routers/dashboard.py` | Edit — add `require_permission` dep (sub-task 5) |
| `app/routers/students.py` | Edit — add `require_permission` dep (sub-task 5) |
| `app/main.py` | Edit — include auth router, register 403 handler (sub-tasks 3+5) |
| `app/config.py` | Edit — add `TOTP_REQUIRED: bool = True` setting |
| `.env.example` | Edit — add `TOTP_REQUIRED=true` |
| `scripts/reset_db.py` | Create (sub-task 6) |
| `tests/test_auth.py` | Create (sub-task 7) |
| `tests/test_smoke.py` | Edit — update `test_dashboard_ok` (sub-task 5) |
