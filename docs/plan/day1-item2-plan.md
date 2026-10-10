# Plan — Day 1 Item 2: Models + Alembic Migration + FK Pragma + Seed Roles/Permissions

**Status:** [ ] pending  
**Source of truth:** `docs/design/DATABASE_SCHEMA.md` > `docs/plan/decisions.md` > `docs/plan/spec.md`

## Overview

Populate `app/models.py` with every SQLAlchemy ORM class defined in DATABASE_SCHEMA.md §5 plus
the spec §3 legacy-field additions (D-19 through D-25). Generate the first Alembic migration
from those models. Verify FK enforcement (already wired in `app/db.py` — test it). Write a
`scripts/seed_roles.py` that inserts the four roles and seven permissions from D-23. Extend
`tests/conftest.py` with an in-memory SQLite fixture. Add `tests/test_schema.py` covering
acceptance checks 1 and 4 from DATABASE_SCHEMA.md §8.

The FK pragma wire is already coded in `app/db.py` (`PRAGMA foreign_keys=ON` on every connect).
This item tests it; no code change to `db.py` is expected.

---

## Sub-Task A — Write `app/models.py`

**Intent:** Define every ORM class so that Alembic `autogenerate` produces a complete,
correct first migration and the acceptance-check tests can run.

**Expected Outcomes:**
- All 12 tables exist as SQLAlchemy model classes (see list below).
- Column types, constraints, and server defaults match DATABASE_SCHEMA.md §5 + spec §3.
- No `create_all` call — Alembic owns schema creation.

**Todo List:**
1. Add `UserAccount` — fields: `id`, `provider`, `provider_subject`, `display_name`, `email`,
   `active`, `created_at`, `updated_at`; unique constraint on `(provider, provider_subject)`.
2. Add `LocalCredential` — `user_account_id` (PK + FK), `password_hash`, `totp_secret_encrypted`,
   `mfa_enabled`, `recovery_codes_hash` (JSON), `failed_logins`, `locked_until`, `updated_at`.
3. Add `Role` — `id`, unique `name`.
4. Add `UserRole` — composite PK `(user_account_id, role_id)`.
5. Add `Permission` — `id`, unique `code`, `description`.
6. Add `RolePermission` — composite PK `(role_id, permission_id)`.
7. Add `Program` — `id`, unique `code`, `name`, `active`, `created_at`, `updated_at`.
8. Add `Student` — `id`, `student_number` (unique, not-nullable, not-updatable via app logic),
   `user_account_id` (nullable unique FK), `first_name`, `last_name`, `email`, `phone` (→
   `home_phone` + `work_phone` per spec §3), `program_id` (nullable FK), `status`
   (CHECK active/inactive/archived), `version INT default 1`,  `created_at`, `updated_at`;
   plus legacy-field additions: `address`, `city`, `state`, `zip`, `high_school`,
   `date_graduated`, `seeking_employment`, `desired_job`, `enrolled_date`, `legacy_source`.
9. Add `Employer` — `id`, `name`, `active`, `created_at`, `updated_at`; legacy additions:
   `address`, `city`, `state`, `zip`, `phone`, `company_type`, `legacy_code`.
10. Add `Employment` — `id`, `student_id` (FK), `employer_id` (FK), `job_title`, `job_type`
    (CHECK part_time/full_time/other/unknown), `hours_per_week` (CHECK >= 0), `start_date`,
    `end_date` (nullable, CHECK end_date >= start_date when both present), `version`,
    `created_at`, `updated_at`; legacy additions: `supervisor`, `hourly_rate NUMERIC(8,2)`.
11. Add `ChangeRequest` — all fields from DATABASE_SCHEMA.md §5 CHANGE_REQUEST.
12. Add `AuditEvent` — `id`, `actor_account_id` (nullable, NOT a real FK — loose reference),
    `event_type`, `entity_type`, `entity_id`, `change_request_id` (nullable), `occurred_at`,
    `detail` (JSON or TEXT).

**Relevant Context:**
- `app/db.py` — `Base` is defined here; models must import and subclass it.
- DATABASE_SCHEMA.md §5 — authoritative field list.
- `docs/plan/spec.md` §3 — legacy-field additions.
- Decisions D-19 (STU-#### format), D-20 (no birth data), D-22 (unknown job_type),
  D-23 (role names), D-25 (Alembic).

**Status:** [ ] pending

---

## Sub-Task B — Generate Alembic initial migration

**Intent:** Produce a single `migrations/versions/0001_initial.py` that captures every table
from Sub-Task A. This is what `alembic upgrade head` runs in Docker and in tests.

**Expected Outcomes:**
- Running `alembic upgrade head` against a blank SQLite file creates all 12 tables.
- Running it a second time is a no-op.

**Todo List:**
1. Confirm `migrations/env.py` imports `app.models` (already done in skeleton — verify).
2. Run `alembic revision --autogenerate -m "initial"` to generate the file.
3. Inspect the generated file; verify all tables and constraints appear. Fix any omissions
   (autogenerate misses server-default-only constructs; add manually if needed).
4. Run `alembic upgrade head` against the dev `onyx.db` to confirm it applies cleanly.

**Relevant Context:**
- `migrations/env.py` — already wired to `app.db.Base` and `app.models`.
- `alembic.ini` — `sqlalchemy.url` is overridden by `env.py` via `DATABASE_URL`.

**Status:** [ ] pending

---

## Sub-Task C — Extend `tests/conftest.py` with DB fixture

**Intent:** Tests need an isolated, in-memory SQLite database with all tables created and FK
pragma enabled. This fixture is reused by all schema tests.

**Expected Outcomes:**
- A `db_session` fixture is available to all tests.
- Each test function gets a fresh session; tables are created from `Base.metadata.create_all`.
- `PRAGMA foreign_keys=ON` fires on the in-memory connection.

**Todo List:**
1. Add an `engine` fixture (scope=`function`) that creates an in-memory SQLite engine,
   applies the FK pragma via `event.listens_for`, and calls `Base.metadata.create_all`.
2. Add a `db_session` fixture that opens a `Session`, yields it, and rolls back / disposes.
3. Keep the existing `client` fixture untouched.

**Relevant Context:**
- `tests/conftest.py` — current state (client fixture only).
- `app/db.py` — FK pragma pattern to replicate in the test engine.

**Status:** [ ] pending

---

## Sub-Task D — Write `tests/test_schema.py` (acceptance checks 1 and 4)

**Intent:** Prove the schema enforces the two checks most critical to Demo Night:
- Check 1: student creation generates a unique immutable number; required-field validation works.
- Check 4: invalid dates and negative hours are rejected; FK failures cannot create orphan rows.

**Expected Outcomes:**
- `pytest -q` passes with no failures.
- Tests document expected behavior clearly for the submission video.

**Todo List:**
1. **Check 1a** — create a `Student` with `first_name`, `last_name`, `student_number`; assert
   the number is stored and unique (a second student with the same number raises `IntegrityError`).
2. **Check 1b** — attempt to create a `Student` with `first_name=None`; assert `IntegrityError`
   (or SQLAlchemy NOT NULL violation).
3. **Check 4a** — create an `Employment` with `hours_per_week = -1`; assert the DB rejects it
   (SQLite CHECK constraint raises `IntegrityError`).
4. **Check 4b** — create an `Employment` with `end_date` < `start_date`; assert rejection.
5. **Check 4c** — attempt to create an `Employment` with a non-existent `student_id`; assert
   `IntegrityError` (FK violation — proves pragma is ON).
6. Each test uses the `db_session` fixture and is independent.

**Relevant Context:**
- DATABASE_SCHEMA.md §8 acceptance checks 1 and 4.
- `tests/test_smoke.py` — style reference.

**Status:** [ ] pending

---

## Sub-Task E — Write `scripts/seed_roles.py`

**Intent:** Idempotent script that inserts the four roles and seven permissions defined in D-23,
and assigns permissions to roles. Runnable standalone and importable by `scripts/seed.py`.

**Expected Outcomes:**
- Running it twice leaves the same rows (no duplicates).
- All four roles exist: Administrator, Staff, Reviewer, Student.
- All seven permissions exist: `students.read`, `students.manage`, `employment.manage`,
  `reports.read`, `accounts.manage`, `student_updates.approve`, `self_service.use`.
- Role→permission assignments match D-23 exactly.

**Todo List:**
1. Define `ROLES` dict and `PERMISSIONS` list from D-23.
2. Define `ROLE_PERMISSIONS` mapping (Administrator → all; Staff → read/manage students +
   employment + reports; Reviewer → approve only; Student → self_service).
3. Use `session.merge()` or `INSERT OR IGNORE`-style upsert so re-runs are safe.
4. Add a `__main__` block so `python scripts/seed_roles.py` works from the repo root.
5. Ensure the script creates the engine from `app.db` (not `Base.metadata.create_all` — tables
   already exist after migration).

**Relevant Context:**
- `docs/plan/decisions.md` D-23 — exact role/permission assignments.
- `scripts/seed.py` — existing file to wire this into later.

**Status:** [ ] pending

---

## Files Changed / Created

| File | Action |
|---|---|
| `app/models.py` | Fill (currently empty) |
| `migrations/versions/0001_initial.py` | Generate via `alembic revision --autogenerate` |
| `tests/conftest.py` | Add `db_session` fixture |
| `tests/test_schema.py` | Create |
| `scripts/seed_roles.py` | Create |

---

## How Clarence Checks It

1. Run `pytest -q` — must show at least **7 passed** (2 existing smoke + 5 new schema tests).
2. Run `alembic upgrade head` — terminal shows `Running upgrade -> <rev>, initial` with no
   errors; `onyx.db` is created (or updated) in the repo root.
3. Run `python scripts/seed_roles.py` — no errors; run it a second time — still no errors.
4. Open `onyx.db` with any SQLite viewer (e.g. DB Browser for SQLite) and confirm all 12 tables
   are present and `student.student_number` has a UNIQUE index.
