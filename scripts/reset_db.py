"""reset_db.py — full database reset: drop → migrate → seed roles →
import 1998 data → seed demo → create two demo users.

Prints sign-in details for both demo accounts at the end.

Usage:
    .venv\\Scripts\\python.exe scripts/reset_db.py

WARNING: This destroys all data in the configured DATABASE_URL.
         Do NOT run against a production database.
"""
from __future__ import annotations

import subprocess
import sys
import os
import uuid

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# ---------------------------------------------------------------------------
# Demo user constants  (also used by tests/test_auth.py)
# ---------------------------------------------------------------------------

ADMIN_EMAIL        = "admin@onyx.demo"
ADMIN_PASSWORD     = "OnyxAdmin2026!"
ADMIN_TOTP_SECRET  = "JBSWY3DPEHPK3PXP"
ADMIN_DISPLAY_NAME = "Demo Admin"

STAFF_EMAIL        = "staff@onyx.demo"
STAFF_PASSWORD     = "OnyxStaff2026!"
STAFF_TOTP_SECRET  = "JBSWY3DPEHPK3PXQ"
STAFF_DISPLAY_NAME = "Demo Staff"

NEWSTAFF_EMAIL        = "newstaff@onyx.demo"
NEWSTAFF_PASSWORD     = "OnyxNew2026!"
NEWSTAFF_DISPLAY_NAME = "New Staff"


# ---------------------------------------------------------------------------
# Step helpers
# ---------------------------------------------------------------------------

def _step(msg: str) -> None:
    print(f"\n{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}")


def _drop_and_migrate() -> None:
    """Drop all tables via Alembic down to base, then upgrade to head."""
    _step("1 / 5  Dropping all tables and re-running migrations")

    # alembic downgrade clears tables; stamp base then upgrade is safer
    # For SQLite we simply delete the file and re-migrate.
    from app.config import get_settings
    settings = get_settings()
    url = settings.DATABASE_URL

    if url.startswith("sqlite:///"):
        db_path = url.replace("sqlite:///", "").replace("/", os.sep)
        # Dispose the engine so Windows releases the file lock
        try:
            from app.db import engine as _engine
            _engine.dispose()
        except Exception:
            pass
        import time
        for attempt in range(5):
            try:
                if os.path.exists(db_path):
                    os.remove(db_path)
                    print(f"  Deleted {db_path}")
                break
            except PermissionError:
                if attempt == 4:
                    raise
                time.sleep(0.5)
        # Also remove WAL/SHM if present
        for suffix in ["-wal", "-shm"]:
            p = db_path + suffix
            if os.path.exists(p):
                try:
                    os.remove(p)
                except PermissionError:
                    pass
    else:
        # PostgreSQL: drop all via alembic downgrade
        result = subprocess.run(
            [sys.executable, "-m", "alembic", "downgrade", "base"],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            print(result.stderr)
            sys.exit(1)

    # Run migrations
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        sys.exit(1)
    print("  Migrations applied.")


def _seed_roles(session) -> None:
    _step("2 / 5  Seeding roles and permissions")
    from scripts.seed_roles import seed
    seed(session)


def _run_legacy_import(session) -> None:
    _step("3 / 5  Importing 1998 legacy data")
    from app.services.legacy_import import run_import
    result = run_import(session)
    print(
        f"  Students created: {result['students_created']}"
        f"  (skipped: {result['students_skipped']})"
    )
    print(f"  Employers created: {result['employers_created']}")
    print(f"  Jobs created:      {result['jobs_created']}")
    print(f"  SSNs discarded:    {result['ssn_count']}")


def _seed_demo(session) -> None:
    _step("4 / 5  Seeding demo students and jobs")
    from scripts.seed_demo import seed
    seed(session)


def _create_demo_users(session) -> None:
    _step("5 / 5  Creating demo user accounts")
    from app.models import LocalCredential, Role, UserAccount, UserRole
    from app.security import hash_password, encrypt_totp_secret

    def _make_user(email, display_name, password, totp_secret, role_name):
        existing = session.query(UserAccount).filter_by(email=email).first()
        if existing:
            print(f"  {email} already exists — skipping.")
            return

        user = UserAccount(
            provider="local",
            provider_subject=str(uuid.uuid4()),
            display_name=display_name,
            email=email,
            active=True,
        )
        session.add(user)
        session.flush()

        cred = LocalCredential(
            user_account_id=user.id,
            password_hash=hash_password(password),
            totp_secret_encrypted=encrypt_totp_secret(totp_secret) if totp_secret else None,
            mfa_enabled=totp_secret is not None,
            recovery_codes_hash=[],
            failed_logins=0,
        )
        session.add(cred)

        role = session.query(Role).filter_by(name=role_name).first()
        if role:
            session.add(UserRole(user_account_id=user.id, role_id=role.id))

        session.flush()
        print(f"  Created {role_name} account: {email}")

    _make_user(ADMIN_EMAIL, ADMIN_DISPLAY_NAME, ADMIN_PASSWORD, ADMIN_TOTP_SECRET, "Administrator")
    _make_user(STAFF_EMAIL, STAFF_DISPLAY_NAME, STAFF_PASSWORD, STAFF_TOTP_SECRET, "Staff")
    _make_user(NEWSTAFF_EMAIL, NEWSTAFF_DISPLAY_NAME, NEWSTAFF_PASSWORD, None, "Staff")
    session.commit()


def _print_summary(session) -> None:
    from app.models import Employment, Student
    total_students = session.query(Student).count()
    total_jobs     = session.query(Employment).count()
    print("\n" + "="*60)
    print("  RESET COMPLETE")
    print("="*60)
    print(f"  Total students : {total_students}")
    print(f"  Total jobs     : {total_jobs}")
    print()
    print("  " + "-"*55)
    print("  DEMO SIGN-IN CREDENTIALS")
    print("  " + "-"*55)
    print(f"  Admin   email : {ADMIN_EMAIL}")
    print(f"          pass  : {ADMIN_PASSWORD}")
    print(f"          TOTP  : {ADMIN_TOTP_SECRET}")
    print("  " + "-"*55)
    print(f"  Staff   email : {STAFF_EMAIL}")
    print(f"          pass  : {STAFF_PASSWORD}")
    print(f"          TOTP  : {STAFF_TOTP_SECRET}")
    print("  " + "-"*55)
    print(f"  NewStaff email : {NEWSTAFF_EMAIL}")
    print(f"           pass  : {NEWSTAFF_PASSWORD}")
    print(f"           TOTP  : (none — will be shown QR setup on first sign-in)")
    print("  " + "-"*55)
    print()
    print("  Scan TOTP secret with an authenticator app,")
    print("  or use: pyotp.TOTP('<secret>').now()")
    print()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    _drop_and_migrate()

    # Import engine/session after migrations so tables exist
    from app.db import engine
    from sqlalchemy.orm import Session

    with Session(engine) as session:
        _seed_roles(session)
        _run_legacy_import(session)
        _seed_demo(session)
        _create_demo_users(session)
        _print_summary(session)
