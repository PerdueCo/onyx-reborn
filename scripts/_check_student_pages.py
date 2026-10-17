"""Quick smoke-check of /students/new and /students/{id}/edit via TestClient."""
import re
import sys

import pyotp
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app as fastapi_app
import app.models as _m  # noqa: F401

SECRET = "JBSWY3DPEHPK3PXP"

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@event.listens_for(engine, "connect")
def _fk(dbapi_conn, _rec):
    c = dbapi_conn.cursor()
    c.execute("PRAGMA foreign_keys=ON")
    c.close()


Base.metadata.create_all(engine)

with Session(engine) as db:
    from scripts.seed_roles import seed
    seed(db)

    from app.models import LocalCredential, Role, UserAccount, UserRole
    from app.security import encrypt_totp_secret, hash_password

    u = UserAccount(
        provider="local",
        provider_subject="check@check.test",
        display_name="Checker",
        email="check@check.test",
        active=True,
    )
    db.add(u)
    db.flush()
    db.add(
        LocalCredential(
            user_account_id=u.id,
            password_hash=hash_password("Check123!"),
            totp_secret_encrypted=encrypt_totp_secret(SECRET),
            mfa_enabled=True,
            recovery_codes_hash=[],
            failed_logins=0,
        )
    )
    role = db.query(Role).filter_by(name="Administrator").first()
    if role:
        db.add(UserRole(user_account_id=u.id, role_id=role.id))
    db.commit()

    def override():
        yield db

    fastapi_app.dependency_overrides[get_db] = override
    ok = True
    with TestClient(fastapi_app, raise_server_exceptions=True) as c:
        # Login
        r1 = c.get("/login")
        csrf = re.search(r'name="csrf_token"\s+value="([^"]+)"', r1.text).group(1)
        c.post(
            "/login",
            data={"email": "check@check.test", "password": "Check123!", "csrf_token": csrf},
            follow_redirects=False,
        )
        r3 = c.get("/mfa/verify")
        csrf2 = re.search(r'name="csrf_token"\s+value="([^"]+)"', r3.text).group(1)
        r4 = c.post(
            "/mfa/verify",
            data={"code": pyotp.TOTP(SECRET).now(), "csrf_token": csrf2},
            follow_redirects=False,
        )
        assert r4.status_code == 303, f"MFA failed: {r4.text[:200]}"

        # /students/new
        rn = c.get("/students/new")
        checks = {
            "status 200": rn.status_code == 200,
            "has csrf_token": 'name="csrf_token"' in rn.text,
            "has first_name field": 'name="first_name"' in rn.text,
            "has Add Student heading": "Add Student" in rn.text,
            "no SSN field": "ssn" not in rn.text.lower(),
        }
        print("/students/new:")
        for k, v in checks.items():
            symbol = "OK" if v else "FAIL"
            print(f"  {symbol}  {k}")
            if not v:
                ok = False

        # Create a student
        csrf3 = re.search(r'name="csrf_token"\s+value="([^"]+)"', rn.text).group(1)
        rc = c.post(
            "/students/new",
            data={"csrf_token": csrf3, "first_name": "Smoke", "last_name": "Test", "status": "active"},
            follow_redirects=False,
        )
        print(f"\nPOST /students/new: status={rc.status_code} (want 303)")
        if rc.status_code != 303:
            ok = False
        sid = rc.headers.get("location", "").rstrip("/").split("/")[-1]

        # /students/{id}/edit
        re_ = c.get(f"/students/{sid}/edit")
        checks2 = {
            "status 200": re_.status_code == 200,
            "has csrf_token": 'name="csrf_token"' in re_.text,
            "has first_name field": 'name="first_name"' in re_.text,
            "student name shown (Smoke)": "Smoke" in re_.text,
            "no SSN field": "ssn" not in re_.text.lower(),
        }
        print(f"\n/students/{sid}/edit:")
        for k, v in checks2.items():
            symbol = "OK" if v else "FAIL"
            print(f"  {symbol}  {k}")
            if not v:
                ok = False

    fastapi_app.dependency_overrides.clear()

sys.exit(0 if ok else 1)
