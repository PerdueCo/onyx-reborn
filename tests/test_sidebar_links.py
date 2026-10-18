"""tests/test_sidebar_links.py — every sidebar link returns 200 for its role.

Acceptance criteria:
  1. Staff user: /dashboard, /students, /employment, /reports → 200
  2. Staff user: /admin → 403
  3. Admin user: all of the above + /admin → 200
  4. /about → 200 (unauthenticated, no session)
  5. Unlock POST clears lockout (locked_until=None, failed_logins=0)
  6. About link present in public landing page topbar
  7. About link present in signed-in sidebar
"""
from __future__ import annotations

import datetime
import re

import pyotp
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app as fastapi_app
from app.models import (
    LocalCredential,
    Role,
    Student,
    UserAccount,
    UserRole,
)
from app.security import encrypt_totp_secret, hash_password

# ---------------------------------------------------------------------------
# Test user credentials
# ---------------------------------------------------------------------------

_STAFF_EMAIL = "sidebar_staff@onyx.test"
_STAFF_PW = "SidebarStaff2026!"
_STAFF_TOTP = "JBSWY3DPEHPK3PXS"

_ADMIN_EMAIL = "sidebar_admin@onyx.test"
_ADMIN_PW = "SidebarAdmin2026!"
_ADMIN_TOTP = "JBSWY3DPEHPK3PXT"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _seed_user(
    db: Session,
    email: str,
    password: str,
    totp_secret: str,
    role_name: str,
    locked: bool = False,
) -> UserAccount:
    user = UserAccount(
        provider="local",
        provider_subject=email,
        display_name=email.split("@")[0],
        email=email,
        active=True,
    )
    db.add(user)
    db.flush()

    cred = LocalCredential(
        user_account_id=user.id,
        password_hash=hash_password(password),
        totp_secret_encrypted=encrypt_totp_secret(totp_secret),
        mfa_enabled=True,
        recovery_codes_hash=[],
        failed_logins=5 if locked else 0,
        locked_until=(
            datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            if locked else None
        ),
    )
    db.add(cred)

    role = db.query(Role).filter_by(name=role_name).first()
    if role:
        db.add(UserRole(user_account_id=user.id, role_id=role.id))

    db.commit()
    return user


@pytest.fixture()
def sidebar_db(db_session: Session) -> Session:
    from scripts.seed_roles import seed as seed_roles
    seed_roles(db_session)
    _seed_user(db_session, _STAFF_EMAIL, _STAFF_PW, _STAFF_TOTP, "Staff")
    _seed_user(db_session, _ADMIN_EMAIL, _ADMIN_PW, _ADMIN_TOTP, "Administrator")
    # Also add a student record so /students returns 200 with data
    db_session.add(
        Student(
            student_number="STU-S001",
            first_name="Sidebar",
            last_name="Student",
            status="active",
        )
    )
    db_session.commit()
    return db_session


def _make_client(db: Session, email: str, password: str, totp: str) -> TestClient:
    """Return a fully signed-in TestClient overriding get_db."""
    from app.db import get_db

    def _override():
        yield db

    fastapi_app.dependency_overrides[get_db] = _override
    c = TestClient(fastapi_app, raise_server_exceptions=True)
    c.__enter__()

    # Login
    r1 = c.get("/login")
    csrf = re.search(r'name="csrf_token"\s+value="([^"]+)"', r1.text).group(1)
    r2 = c.post(
        "/login",
        data={"email": email, "password": password, "csrf_token": csrf},
        follow_redirects=False,
    )
    assert r2.status_code == 303, f"Login failed: {r2.text[:300]}"

    # MFA
    r3 = c.get("/mfa/verify")
    csrf2 = re.search(r'name="csrf_token"\s+value="([^"]+)"', r3.text).group(1)
    code = pyotp.TOTP(totp).now()
    r4 = c.post(
        "/mfa/verify",
        data={"code": code, "csrf_token": csrf2},
        follow_redirects=False,
    )
    assert r4.status_code == 303, f"MFA failed: {r4.text[:300]}"
    return c


@pytest.fixture()
def staff_client(sidebar_db: Session):
    c = _make_client(sidebar_db, _STAFF_EMAIL, _STAFF_PW, _STAFF_TOTP)
    yield c
    c.__exit__(None, None, None)
    fastapi_app.dependency_overrides.clear()


@pytest.fixture()
def admin_client(sidebar_db: Session):
    c = _make_client(sidebar_db, _ADMIN_EMAIL, _ADMIN_PW, _ADMIN_TOTP)
    yield c
    c.__exit__(None, None, None)
    fastapi_app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Tests — /about (public)
# ---------------------------------------------------------------------------

def test_about_page_200_unauthenticated(client):
    """/about returns 200 without a session."""
    r = client.get("/about")
    assert r.status_code == 200
    assert "About" in r.text


def test_about_link_in_landing_topbar(client):
    """Landing page topbar contains an /about link."""
    r = client.get("/")
    assert r.status_code == 200
    assert 'href="/about"' in r.text


# ---------------------------------------------------------------------------
# Tests — Staff sidebar links
# ---------------------------------------------------------------------------

def test_staff_dashboard_200(staff_client: TestClient):
    r = staff_client.get("/dashboard")
    assert r.status_code == 200


def test_staff_students_200(staff_client: TestClient):
    r = staff_client.get("/students")
    assert r.status_code == 200


def test_staff_employment_200(staff_client: TestClient):
    """/employment overview returns 200 for Staff."""
    r = staff_client.get("/employment")
    assert r.status_code == 200
    # Should show both tabs
    assert "Current Jobs" in r.text
    assert "Employers" in r.text


def test_staff_employment_jobs_tab_200(staff_client: TestClient):
    r = staff_client.get("/employment?tab=jobs")
    assert r.status_code == 200


def test_staff_employment_employers_tab_200(staff_client: TestClient):
    r = staff_client.get("/employment?tab=employers")
    assert r.status_code == 200
    assert "Add Employer" in r.text


def test_staff_reports_200(staff_client: TestClient):
    r = staff_client.get("/reports")
    assert r.status_code == 200


def test_staff_admin_403(staff_client: TestClient):
    """/admin must return 403 for Staff (no accounts.manage permission)."""
    r = staff_client.get("/admin")
    assert r.status_code == 403


def test_staff_sidebar_has_about_link(staff_client: TestClient):
    """Signed-in sidebar contains 'About Onyx' link to /about."""
    r = staff_client.get("/dashboard")
    assert r.status_code == 200
    assert 'href="/about"' in r.text


# ---------------------------------------------------------------------------
# Tests — Admin sidebar links
# ---------------------------------------------------------------------------

def test_admin_dashboard_200(admin_client: TestClient):
    r = admin_client.get("/dashboard")
    assert r.status_code == 200


def test_admin_students_200(admin_client: TestClient):
    r = admin_client.get("/students")
    assert r.status_code == 200


def test_admin_employment_200(admin_client: TestClient):
    r = admin_client.get("/employment")
    assert r.status_code == 200


def test_admin_reports_200(admin_client: TestClient):
    r = admin_client.get("/reports")
    assert r.status_code == 200


def test_admin_admin_200(admin_client: TestClient):
    """/admin returns 200 for Administrator."""
    r = admin_client.get("/admin")
    assert r.status_code == 200
    assert "Users" in r.text
    assert "Recent audit log" in r.text


def test_admin_page_shows_users_table(admin_client: TestClient):
    """Admin page contains a table with user rows."""
    r = admin_client.get("/admin")
    assert r.status_code == 200
    # Both seeded users should appear
    assert _STAFF_EMAIL in r.text or "sidebar_staff" in r.text
    assert _ADMIN_EMAIL in r.text or "sidebar_admin" in r.text


# ---------------------------------------------------------------------------
# Tests — Unlock
# ---------------------------------------------------------------------------

def test_unlock_clears_lockout(sidebar_db: Session):
    """POST /admin/unlock/{id} resets locked_until and failed_logins to 0."""
    from app.db import get_db

    # Seed a locked Staff user
    locked_user = _seed_user(
        sidebar_db,
        "locked_staff@onyx.test",
        "LockedPass2026!",
        "JBSWY3DPEHPK3PXU",
        "Staff",
        locked=True,
    )
    locked_cred = sidebar_db.get(LocalCredential, locked_user.id)
    assert locked_cred.locked_until is not None

    def _override():
        yield sidebar_db

    fastapi_app.dependency_overrides[get_db] = _override
    try:
        c = TestClient(fastapi_app, raise_server_exceptions=True)
        with c:
            # Sign in as Admin
            r1 = c.get("/login")
            csrf = re.search(r'name="csrf_token"\s+value="([^"]+)"', r1.text).group(1)
            r2 = c.post(
                "/login",
                data={"email": _ADMIN_EMAIL, "password": _ADMIN_PW, "csrf_token": csrf},
                follow_redirects=False,
            )
            assert r2.status_code == 303
            r3 = c.get("/mfa/verify")
            csrf2 = re.search(r'name="csrf_token"\s+value="([^"]+)"', r3.text).group(1)
            code = pyotp.TOTP(_ADMIN_TOTP).now()
            r4 = c.post(
                "/mfa/verify",
                data={"code": code, "csrf_token": csrf2},
                follow_redirects=False,
            )
            assert r4.status_code == 303

            # Get CSRF from admin page
            r5 = c.get("/admin")
            assert r5.status_code == 200
            csrf3 = re.search(r'name="csrf_token"\s+value="([^"]+)"', r5.text).group(1)

            # POST unlock
            r6 = c.post(
                f"/admin/unlock/{locked_user.id}",
                data={"csrf_token": csrf3},
                follow_redirects=False,
            )
            assert r6.status_code == 303, f"Expected 303 redirect, got {r6.status_code}: {r6.text[:300]}"

        # Verify DB: credential cleared
        sidebar_db.expire(locked_cred)
        sidebar_db.refresh(locked_cred)
        assert locked_cred.locked_until is None, "locked_until should be None after unlock"
        assert locked_cred.failed_logins == 0, "failed_logins should be 0 after unlock"
    finally:
        fastapi_app.dependency_overrides.clear()


def test_unlock_writes_audit_event(sidebar_db: Session):
    """POST /admin/unlock/{id} creates an account_unlock audit event."""
    from app.db import get_db
    from app.models import AuditEvent

    locked_user2 = _seed_user(
        sidebar_db,
        "locked_staff2@onyx.test",
        "LockedPass2026!",
        "JBSWY3DPEHPK3PXV",
        "Staff",
        locked=True,
    )

    def _override():
        yield sidebar_db

    fastapi_app.dependency_overrides[get_db] = _override
    try:
        c = TestClient(fastapi_app, raise_server_exceptions=True)
        with c:
            r1 = c.get("/login")
            csrf = re.search(r'name="csrf_token"\s+value="([^"]+)"', r1.text).group(1)
            c.post(
                "/login",
                data={"email": _ADMIN_EMAIL, "password": _ADMIN_PW, "csrf_token": csrf},
                follow_redirects=False,
            )
            r3 = c.get("/mfa/verify")
            csrf2 = re.search(r'name="csrf_token"\s+value="([^"]+)"', r3.text).group(1)
            code = pyotp.TOTP(_ADMIN_TOTP).now()
            c.post("/mfa/verify", data={"code": code, "csrf_token": csrf2},
                   follow_redirects=False)

            r5 = c.get("/admin")
            csrf3 = re.search(r'name="csrf_token"\s+value="([^"]+)"', r5.text).group(1)
            c.post(
                f"/admin/unlock/{locked_user2.id}",
                data={"csrf_token": csrf3},
                follow_redirects=False,
            )

        # An account_unlock audit event must exist
        ev = (
            sidebar_db.query(AuditEvent)
            .filter_by(event_type="account_unlock", entity_id=locked_user2.id)
            .first()
        )
        assert ev is not None, "account_unlock audit event not found"
    finally:
        fastapi_app.dependency_overrides.clear()
