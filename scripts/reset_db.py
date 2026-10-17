"""reset_db.py — wipe and re-seed the database with demo accounts.

Run this before a demo to get a clean DB with known credentials.
Only creates demo users when DEMO_MODE=true (the default in .env).

Usage:
    .venv\\Scripts\\python.exe scripts/reset_db.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import app.models  # noqa: F401 — registers all ORM classes
from app.db import Base, engine
from app.models import (
    LocalCredential,
    Permission,
    Program,
    Role,
    RolePermission,
    UserAccount,
    UserRole,
)
from app.security import encrypt_totp_secret, hash_password
from scripts.seed_roles import seed as seed_roles
from sqlalchemy.orm import Session

# ---------------------------------------------------------------------------
# Known demo credentials (printed to stdout for judges)
# ---------------------------------------------------------------------------

DEMO_USERS = [
    {
        "email": "admin@onyx.demo",
        "display_name": "Demo Admin",
        "password": "OnyxAdmin2026!",
        "totp_secret": "JBSWY3DPEHPK3PXP",   # well-known test secret
        "role": "Administrator",
    },
    {
        "email": "staff@onyx.demo",
        "display_name": "Demo Staff",
        "password": "OnyxStaff2026!",
        "totp_secret": "JBSWY3DPEHPK3PXQ",   # well-known test secret
        "role": "Staff",
    },
]

PROGRAMS = [
    ("CIS101", "Computer Information Systems"),
    ("ACC110", "Accounting"),
    ("BUS201", "Business Administration"),
    ("MKT130", "Marketing"),
    ("OFT120", "Office Technology"),
]


def reset(demo_mode: bool = True) -> None:
    print("Dropping all tables…")
    Base.metadata.drop_all(engine)
    print("Creating all tables…")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        # Roles + permissions
        seed_roles(session)

        # Programs
        for code, name in PROGRAMS:
            if not session.query(Program).filter_by(code=code).first():
                session.add(Program(code=code, name=name, active=True))
        session.commit()
        print(f"Seeded {len(PROGRAMS)} programs.")

        if demo_mode:
            _create_demo_users(session)
        else:
            print("DEMO_MODE=false — skipping demo user creation.")


def _create_demo_users(session: Session) -> None:
    print()
    print("─" * 57)
    print("  Onyx Reborn demo accounts")
    print("─" * 57)

    for spec in DEMO_USERS:
        role_obj = session.query(Role).filter_by(name=spec["role"]).first()
        if not role_obj:
            print(f"  WARNING: role '{spec['role']}' not found — skipping {spec['email']}")
            continue

        user = UserAccount(
            provider="local",
            provider_subject=spec["email"],
            display_name=spec["display_name"],
            email=spec["email"],
            active=True,
        )
        session.add(user)
        session.flush()

        # Encrypt TOTP secret using the MFA_ENC_KEY from settings
        enc_secret = encrypt_totp_secret(spec["totp_secret"])
        _, hashed_codes = _empty_recovery_codes()

        cred = LocalCredential(
            user_account_id=user.id,
            password_hash=hash_password(spec["password"]),
            totp_secret_encrypted=enc_secret,
            mfa_enabled=True,
            recovery_codes_hash=hashed_codes,
            failed_logins=0,
        )
        session.add(cred)

        # Assign role
        session.add(UserRole(user_account_id=user.id, role_id=role_obj.id))
        session.flush()

        print(f"  {spec['email']}")
        print(f"    password   : {spec['password']}")
        print(f"    TOTP secret: {spec['totp_secret']}")
        print(f"    role       : {spec['role']}")
        print()

    session.commit()
    print("─" * 57)
    print("  Add the TOTP secret to Google/Microsoft Authenticator")
    print("  or any TOTP app using 'Enter setup key'.")
    print("─" * 57)
    print()


def _empty_recovery_codes() -> tuple[list[str], list[str]]:
    """Return (plaintext, hashes) for 8 recovery codes.

    For the demo reset we generate real codes so judges can use them.
    The plaintext is printed separately if needed; here we just need hashes.
    """
    from app.security import generate_recovery_codes
    return generate_recovery_codes()


if __name__ == "__main__":
    from app.config import get_settings
    settings = get_settings()
    reset(demo_mode=settings.DEMO_MODE)
