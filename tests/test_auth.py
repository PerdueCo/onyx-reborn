"""tests/test_auth.py — authentication acceptance tests.

D-30: 2-step always required; tests generate real TOTP codes via
pyotp.TOTP(secret).now() from the seeded known secret — no bypass.

All tests use login_as() which performs real POST /login + POST /mfa/verify.
"""
from __future__ import annotations

import datetime

import pyotp
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app as fastapi_app
from app.models import LocalCredential, Role, UserAccount, UserRole
from app.security import hash_password, encrypt_totp_secret

# ---------------------------------------------------------------------------
# Constants matching reset_db.py
# ---------------------------------------------------------------------------

ADMIN_EMAIL = "admin@onyx.demo"
ADMIN_PASSWORD = "OnyxAdmin2026!"
ADMIN_TOTP_SECRET = "JBSWY3DPEHPK3PXP"

STAFF_EMAIL = "staff@onyx.demo"
STAFF_PASSWORD = "OnyxStaff2026!"
STAFF_TOTP_SECRET = "JBSWY3DPEHPK3PXQ"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def auth_db(db_session: Session) -> Session:
    """Seed admin + staff users into the in-memory DB used by the test client.

    Roles and permissions are seeded inline so this fixture is self-contained.
    """
    from scripts.seed_roles import seed as seed_roles
    seed_roles(db_session)

    _make_user(db_session, ADMIN_EMAIL, "Demo Admin", ADMIN_PASSWORD,
               ADMIN_TOTP_SECRET, "Administrator")
    _make_user(db_session, STAFF_EMAIL, "Demo Staff", STAFF_PASSWORD,
               STAFF_TOTP_SECRET, "Staff")
    db_session.commit()
    return db_session


def _make_user(
    db: Session,
    email: str,
    display_name: str,
    password: str,
    totp_secret: str,
    role_name: str,
) -> UserAccount:
    user = UserAccount(
        provider="local",
        provider_subject=email,
        display_name=display_name,
        email=email,
        active=True,
    )
    db.add(user)
    db.flush()

    enc_secret = encrypt_totp_secret(totp_secret)
    cred = LocalCredential(
        user_account_id=user.id,
        password_hash=hash_password(password),
        totp_secret_encrypted=enc_secret,
        mfa_enabled=True,
        recovery_codes_hash=[],
        failed_logins=0,
    )
    db.add(cred)

    role = db.query(Role).filter_by(name=role_name).first()
    if role:
        db.add(UserRole(user_account_id=user.id, role_id=role.id))
    db.flush()
    return user


@pytest.fixture()
def auth_client(auth_db: Session):
    """TestClient backed by the seeded in-memory DB.

    Overrides get_db so all routes see the same seeded session.
    """
    from app.db import get_db
    def _override():
        yield auth_db
    fastapi_app.dependency_overrides[get_db] = _override
    with TestClient(fastapi_app, raise_server_exceptions=True) as c:
        yield c
    fastapi_app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Helper: login_as
# ---------------------------------------------------------------------------

def _get_csrf(client: TestClient, url: str) -> str:
    """GET a page and extract the csrf_token hidden field value."""
    r = client.get(url)
    # csrf value is in the session cookie — fetch by hitting GET /login and
    # then reading the session that was set
    return ""   # TestClient auto-sends session cookies; csrf is in session


def login_as(client: TestClient, email: str, password: str, totp_secret: str) -> None:
    """Perform a real POST /login + POST /mfa/verify, leaving the client signed in."""
    # Step 1: GET /login to initialise a session with a CSRF token
    r1 = client.get("/login")
    assert r1.status_code == 200

    # Extract csrf from the hidden field in the response HTML
    import re
    m = re.search(r'name="csrf_token"\s+value="([^"]+)"', r1.text)
    assert m, f"CSRF token not found in login page. Got:\n{r1.text[:500]}"
    csrf = m.group(1)

    # Step 2: POST /login
    r2 = client.post(
        "/login",
        data={"email": email, "password": password, "csrf_token": csrf},
        follow_redirects=False,
    )
    assert r2.status_code == 303, f"Expected 303 after login, got {r2.status_code}: {r2.text[:300]}"
    assert "/mfa/verify" in r2.headers.get("location", ""), (
        f"Expected redirect to /mfa/verify, got {r2.headers.get('location')}"
    )

    # Step 3: GET /mfa/verify to get a fresh CSRF for the verify form
    r3 = client.get("/mfa/verify")
    assert r3.status_code == 200
    m2 = re.search(r'name="csrf_token"\s+value="([^"]+)"', r3.text)
    assert m2, "CSRF token not found in mfa/verify page"
    csrf2 = m2.group(1)

    # Step 4: POST /mfa/verify with a freshly-generated TOTP code
    code = pyotp.TOTP(totp_secret).now()
    r4 = client.post(
        "/mfa/verify",
        data={"code": code, "csrf_token": csrf2},
        follow_redirects=False,
    )
    assert r4.status_code == 303, (
        f"Expected 303 after MFA verify, got {r4.status_code}: {r4.text[:300]}"
    )
    assert "/dashboard" in r4.headers.get("location", ""), (
        f"Expected redirect to /dashboard, got {r4.headers.get('location')}"
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_login_ok(auth_client: TestClient):
    """Correct credentials → 303 to /mfa/verify."""
    r = auth_client.get("/login")
    import re
    csrf = re.search(r'name="csrf_token"\s+value="([^"]+)"', r.text).group(1)
    r2 = auth_client.post(
        "/login",
        data={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD, "csrf_token": csrf},
        follow_redirects=False,
    )
    assert r2.status_code == 303
    assert "/mfa/verify" in r2.headers.get("location", "")


def test_login_wrong_password(auth_client: TestClient):
    """Wrong password → 200 with error message, no redirect."""
    r = auth_client.get("/login")
    import re
    csrf = re.search(r'name="csrf_token"\s+value="([^"]+)"', r.text).group(1)
    r2 = auth_client.post(
        "/login",
        data={"email": ADMIN_EMAIL, "password": "WRONG", "csrf_token": csrf},
        follow_redirects=False,
    )
    assert r2.status_code == 200
    assert "incorrect" in r2.text.lower()


def test_login_lockout(auth_client: TestClient, auth_db: Session):
    """5 consecutive bad passwords → account locked message."""
    import re
    for _ in range(5):
        r = auth_client.get("/login")
        csrf = re.search(r'name="csrf_token"\s+value="([^"]+)"', r.text).group(1)
        auth_client.post(
            "/login",
            data={"email": STAFF_EMAIL, "password": "WRONG", "csrf_token": csrf},
        )
    # 6th attempt should show locked
    r = auth_client.get("/login")
    csrf = re.search(r'name="csrf_token"\s+value="([^"]+)"', r.text).group(1)
    r2 = auth_client.post(
        "/login",
        data={"email": STAFF_EMAIL, "password": "WRONG", "csrf_token": csrf},
        follow_redirects=False,
    )
    assert r2.status_code == 200
    assert "locked" in r2.text.lower()


def test_login_locked_account_still_rejected(auth_client: TestClient, auth_db: Session):
    """Account already locked → correct password still rejected with locked msg."""
    import re
    # Force lock directly in the DB
    user = auth_db.query(UserAccount).filter_by(email=ADMIN_EMAIL).first()
    cred = auth_db.get(LocalCredential, user.id)
    cred.locked_until = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    cred.failed_logins = 5
    auth_db.commit()

    r = auth_client.get("/login")
    csrf = re.search(r'name="csrf_token"\s+value="([^"]+)"', r.text).group(1)
    r2 = auth_client.post(
        "/login",
        data={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD, "csrf_token": csrf},
        follow_redirects=False,
    )
    assert r2.status_code == 200
    assert "locked" in r2.text.lower()


def test_totp_correct(auth_client: TestClient):
    """Full login + correct TOTP → session mfa_ok, redirect to /dashboard."""
    login_as(auth_client, ADMIN_EMAIL, ADMIN_PASSWORD, ADMIN_TOTP_SECRET)
    r = auth_client.get("/dashboard", follow_redirects=False)
    assert r.status_code == 200


def test_totp_wrong(auth_client: TestClient):
    """After password ok, a clearly-invalid 6-char non-numeric code → stays on verify page."""
    import re
    r = auth_client.get("/login")
    csrf = re.search(r'name="csrf_token"\s+value="([^"]+)"', r.text).group(1)
    auth_client.post(
        "/login",
        data={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD, "csrf_token": csrf},
        follow_redirects=True,
    )
    r2 = auth_client.get("/mfa/verify")
    csrf2 = re.search(r'name="csrf_token"\s+value="([^"]+)"', r2.text).group(1)
    # Use an obviously invalid code that can never be a valid TOTP
    r3 = auth_client.post(
        "/mfa/verify",
        data={"code": "XXXXXX", "csrf_token": csrf2},
        follow_redirects=False,
    )
    assert r3.status_code == 200
    # Still showing the verify page (not redirected to dashboard)
    assert "Verify" in r3.text


def test_recovery_code_works(auth_client: TestClient, auth_db: Session):
    """A valid recovery code completes MFA and is consumed."""
    import re
    from app.security import generate_recovery_codes

    # Plant a known recovery code on the admin account
    user = auth_db.query(UserAccount).filter_by(email=ADMIN_EMAIL).first()
    cred = auth_db.get(LocalCredential, user.id)
    plain_codes, hashed_codes = generate_recovery_codes()
    cred.recovery_codes_hash = hashed_codes
    auth_db.commit()

    # Log in with password
    r = auth_client.get("/login")
    csrf = re.search(r'name="csrf_token"\s+value="([^"]+)"', r.text).group(1)
    auth_client.post(
        "/login",
        data={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD, "csrf_token": csrf},
        follow_redirects=True,
    )

    # Submit first recovery code
    r2 = auth_client.get("/mfa/verify")
    csrf2 = re.search(r'name="csrf_token"\s+value="([^"]+)"', r2.text).group(1)
    r3 = auth_client.post(
        "/mfa/verify",
        data={"code": plain_codes[0], "csrf_token": csrf2},
        follow_redirects=False,
    )
    assert r3.status_code == 303
    assert "/dashboard" in r3.headers.get("location", "")

    # Recovery code is consumed
    auth_db.refresh(cred)
    assert len(cred.recovery_codes_hash) == 7


def test_logout(auth_client: TestClient):
    """POST /logout clears session, redirects to /."""
    import re
    login_as(auth_client, STAFF_EMAIL, STAFF_PASSWORD, STAFF_TOTP_SECRET)

    # Get a page to harvest a csrf token
    r = auth_client.get("/dashboard")
    csrf = re.search(r'name="csrf_token"\s+value="([^"]+)"', r.text)
    # csrf is embedded by base.html sign-out form
    assert csrf, "No csrf_token found in dashboard page"
    csrf_val = csrf.group(1)

    r2 = auth_client.post(
        "/logout",
        data={"csrf_token": csrf_val},
        follow_redirects=False,
    )
    assert r2.status_code == 303
    assert r2.headers.get("location", "").startswith("/")

    # After logout, /dashboard redirects to /login
    r3 = auth_client.get("/dashboard", follow_redirects=False)
    assert r3.status_code == 303
    assert "/login" in r3.headers.get("location", "")


def test_require_permission_redirects_unauthenticated(auth_client: TestClient):
    """Unauthenticated GET /students → 303 to /login."""
    r = auth_client.get("/students", follow_redirects=False)
    assert r.status_code == 303
    assert "/login" in r.headers.get("location", "")


def test_403_wrong_role(auth_client: TestClient, auth_db: Session):
    """A user with only 'self_service.use' cannot access /students → 403."""
    # Create a Student-role user
    _make_user(auth_db, "student@onyx.demo", "Demo Student", "StudentPass1!",
               "JBSWY3DPEHPK3PXR", "Student")
    auth_db.commit()

    # Use login_as helper to get fully signed-in session
    login_as(auth_client, "student@onyx.demo", "StudentPass1!", "JBSWY3DPEHPK3PXR")

    r3 = auth_client.get("/students", follow_redirects=False)
    assert r3.status_code == 403


# ---------------------------------------------------------------------------
# Test: startup guard raises clearly when MFA_ENC_KEY is missing
# ---------------------------------------------------------------------------

def test_missing_mfa_enc_key_raises_clearly():
    """_require() raises RuntimeError with a clear message when key is empty."""
    from app.config import _require
    try:
        _require("", "MFA_ENC_KEY")
        assert False, "_require should have raised RuntimeError"
    except RuntimeError as e:
        msg = str(e)
        assert "MFA_ENC_KEY" in msg
        assert ".env" in msg


def test_missing_session_secret_raises_clearly():
    """_require() raises RuntimeError with a clear message when SESSION_SECRET is empty."""
    from app.config import _require
    try:
        _require("", "SESSION_SECRET")
        assert False, "_require should have raised RuntimeError"
    except RuntimeError as e:
        msg = str(e)
        assert "SESSION_SECRET" in msg
        assert ".env" in msg


# ---------------------------------------------------------------------------
# Test: unenrolled user is redirected to /mfa/setup, not /mfa/verify
# ---------------------------------------------------------------------------

def test_unenrolled_user_goes_to_mfa_setup(auth_client: TestClient, auth_db: Session):
    """A user with mfa_enabled=False is sent to /mfa/setup after correct password."""
    import re

    # Create a staff user WITHOUT MFA enrolled
    user = UserAccount(
        provider="local",
        provider_subject="newstaff@onyx.demo",
        display_name="New Staff",
        email="newstaff@onyx.demo",
        active=True,
    )
    auth_db.add(user)
    auth_db.flush()

    from app.models import Role
    staff_role = auth_db.query(Role).filter_by(name="Staff").first()
    cred = LocalCredential(
        user_account_id=user.id,
        password_hash=hash_password("NewStaff2026!"),
        mfa_enabled=False,       # <-- not enrolled
        totp_secret_encrypted=None,
        recovery_codes_hash=[],
        failed_logins=0,
    )
    auth_db.add(cred)
    if staff_role:
        auth_db.add(UserRole(user_account_id=user.id, role_id=staff_role.id))
    auth_db.commit()

    # POST /login with correct password
    r = auth_client.get("/login")
    csrf = re.search(r'name="csrf_token"\s+value="([^"]+)"', r.text).group(1)
    r2 = auth_client.post(
        "/login",
        data={"email": "newstaff@onyx.demo", "password": "NewStaff2026!", "csrf_token": csrf},
        follow_redirects=False,
    )
    assert r2.status_code == 303
    assert "/mfa/setup" in r2.headers.get("location", ""), (
        f"Expected redirect to /mfa/setup, got {r2.headers.get('location')}"
    )

    # GET /mfa/setup should return 200 with QR code
    r3 = auth_client.get("/mfa/setup")
    assert r3.status_code == 200
    assert "Set up" in r3.text
    assert "data:image/png;base64," in r3.text

    # Sign In button should NOT appear on /mfa/setup
    assert 'href="/login"' not in r3.text or "Sign in" not in r3.text


def test_login_page_has_no_sign_in_button_in_topbar(auth_client: TestClient):
    """The 'Sign in' button in the topbar must be hidden on /login."""
    r = auth_client.get("/login")
    assert r.status_code == 200
    # The topbar_right block is empty — the topbar-signin anchor must not appear
    assert 'class="btn btn-primary btn-sm topbar-signin"' not in r.text
