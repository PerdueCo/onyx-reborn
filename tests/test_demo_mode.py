"""tests/test_demo_mode.py — demo-mode sign-in helper acceptance tests.

Requirements:
  1. /login "Try the demo" box with "Try as Staff" / "Try as Administrator" buttons
     appears when DEMO_MODE=true, absent when DEMO_MODE=false.
  2. /mfa/verify shows a "Demo account — current code" box (with a live pyotp code
     and a "Use demo code" button) for admin@onyx.demo and staff@onyx.demo only,
     when DEMO_MODE=true.  Absent when DEMO_MODE=false or for other users.
  3. reset_db constants: newstaff@onyx.demo created with mfa_enabled=False,
     no totp_secret, password OnyxNew2026!, Staff role → first sign-in goes to
     /mfa/setup not /mfa/verify.
"""
from __future__ import annotations

import re
import uuid
from unittest.mock import patch

import pyotp
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app as fastapi_app
from app.models import LocalCredential, Role, UserAccount, UserRole
from app.security import encrypt_totp_secret, hash_password

# ---------------------------------------------------------------------------
# Constants matching reset_db.py (import directly to stay DRY)
# ---------------------------------------------------------------------------
from scripts.reset_db import (
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
    ADMIN_TOTP_SECRET,
    NEWSTAFF_EMAIL,
    NEWSTAFF_PASSWORD,
    STAFF_EMAIL,
    STAFF_PASSWORD,
    STAFF_TOTP_SECRET,
)

# ---------------------------------------------------------------------------
# Shared fixture helpers
# ---------------------------------------------------------------------------


def _add_user(
    db: Session,
    email: str,
    display_name: str,
    password: str,
    totp_secret: str | None,
    role_name: str,
) -> UserAccount:
    user = UserAccount(
        provider="local",
        provider_subject=str(uuid.uuid4()),
        display_name=display_name,
        email=email,
        active=True,
    )
    db.add(user)
    db.flush()

    cred = LocalCredential(
        user_account_id=user.id,
        password_hash=hash_password(password),
        totp_secret_encrypted=encrypt_totp_secret(totp_secret) if totp_secret else None,
        mfa_enabled=totp_secret is not None,
        recovery_codes_hash=[],
        failed_logins=0,
    )
    db.add(cred)

    role = db.query(Role).filter_by(name=role_name).first()
    if role:
        db.add(UserRole(user_account_id=user.id, role_id=role.id))
    db.flush()
    return user


def _csrf(response) -> str:
    m = re.search(r'name="csrf_token"\s+value="([^"]+)"', response.text)
    assert m, f"No csrf_token found. Body snippet:\n{response.text[:400]}"
    return m.group(1)


# ---------------------------------------------------------------------------
# Base fixture: seeded DB + client (DEMO_MODE can be overridden per test)
# ---------------------------------------------------------------------------


@pytest.fixture()
def demo_db(db_session: Session) -> Session:
    from scripts.seed_roles import seed as seed_roles
    seed_roles(db_session)

    _add_user(db_session, ADMIN_EMAIL, "Demo Admin", ADMIN_PASSWORD, ADMIN_TOTP_SECRET, "Administrator")
    _add_user(db_session, STAFF_EMAIL, "Demo Staff", STAFF_PASSWORD, STAFF_TOTP_SECRET, "Staff")
    _add_user(db_session, NEWSTAFF_EMAIL, "New Staff", NEWSTAFF_PASSWORD, None, "Staff")
    db_session.commit()
    return db_session


@pytest.fixture()
def demo_client(demo_db: Session):
    from app.db import get_db
    def _override():
        yield demo_db
    fastapi_app.dependency_overrides[get_db] = _override
    with TestClient(fastapi_app, raise_server_exceptions=True) as c:
        yield c
    fastapi_app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# 1. /login — "Try the demo" box
# ---------------------------------------------------------------------------


def test_login_demo_box_present_when_demo_mode_true(demo_client: TestClient):
    """DEMO_MODE=true → login page shows Try as Staff and Try as Administrator buttons."""
    with patch("app.routers.auth.get_settings") as mock_settings:
        mock_settings.return_value.DEMO_MODE = True
        r = demo_client.get("/login")
    assert r.status_code == 200
    assert "Try the demo" in r.text
    assert "Try as Staff" in r.text
    assert "Try as Administrator" in r.text


def test_login_demo_box_absent_when_demo_mode_false(demo_client: TestClient):
    """DEMO_MODE=false → login page has no demo box at all."""
    with patch("app.routers.auth.get_settings") as mock_settings:
        mock_settings.return_value.DEMO_MODE = False
        r = demo_client.get("/login")
    assert r.status_code == 200
    assert "Try the demo" not in r.text
    assert "Try as Staff" not in r.text
    assert "Try as Administrator" not in r.text


def test_login_demo_buttons_include_csrf(demo_client: TestClient):
    """Each demo button form includes a csrf_token hidden field."""
    with patch("app.routers.auth.get_settings") as mock_settings:
        mock_settings.return_value.DEMO_MODE = True
        r = demo_client.get("/login")
    assert r.status_code == 200
    # There should be at least 3 csrf_token fields: main form + 2 demo forms
    csrf_count = len(re.findall(r'name="csrf_token"', r.text))
    assert csrf_count >= 3, f"Expected ≥3 csrf_token fields, found {csrf_count}"


def test_login_demo_staff_button_submits_correct_credentials(demo_client: TestClient):
    """'Try as Staff' button posts staff credentials and reaches /mfa/verify."""
    r1 = demo_client.get("/login")
    csrf = _csrf(r1)

    r2 = demo_client.post(
        "/login",
        data={"email": STAFF_EMAIL, "password": STAFF_PASSWORD, "csrf_token": csrf},
        follow_redirects=False,
    )
    assert r2.status_code == 303
    assert "/mfa/verify" in r2.headers.get("location", "")


def test_login_demo_admin_button_submits_correct_credentials(demo_client: TestClient):
    """'Try as Administrator' button posts admin credentials and reaches /mfa/verify."""
    r1 = demo_client.get("/login")
    csrf = _csrf(r1)

    r2 = demo_client.post(
        "/login",
        data={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD, "csrf_token": csrf},
        follow_redirects=False,
    )
    assert r2.status_code == 303
    assert "/mfa/verify" in r2.headers.get("location", "")


# ---------------------------------------------------------------------------
# 2. /mfa/verify — demo code hint
# ---------------------------------------------------------------------------


def _login_password_step(client: TestClient, email: str, password: str) -> None:
    """POST /login (password step only), leave session at mfa_pending state."""
    r1 = client.get("/login")
    csrf = _csrf(r1)
    r2 = client.post(
        "/login",
        data={"email": email, "password": password, "csrf_token": csrf},
        follow_redirects=False,
    )
    assert r2.status_code == 303


def test_mfa_verify_demo_hint_shown_for_admin(demo_client: TestClient):
    """DEMO_MODE=true + admin signed in at password step → demo code box visible."""
    _login_password_step(demo_client, ADMIN_EMAIL, ADMIN_PASSWORD)
    with patch("app.routers.auth.get_settings") as mock_settings:
        mock_settings.return_value.DEMO_MODE = True
        r = demo_client.get("/mfa/verify")
    assert r.status_code == 200
    assert "Demo account" in r.text
    assert "Use demo code" in r.text
    # The code displayed must be a 6-digit string matching pyotp
    code_match = re.search(r'name="code"\s+value="(\d{6})"', r.text)
    assert code_match, "Hidden demo code input not found"
    assert pyotp.TOTP(ADMIN_TOTP_SECRET).verify(code_match.group(1), valid_window=2)


def test_mfa_verify_demo_hint_shown_for_staff(demo_client: TestClient):
    """DEMO_MODE=true + staff signed in at password step → demo code box visible."""
    _login_password_step(demo_client, STAFF_EMAIL, STAFF_PASSWORD)
    with patch("app.routers.auth.get_settings") as mock_settings:
        mock_settings.return_value.DEMO_MODE = True
        r = demo_client.get("/mfa/verify")
    assert r.status_code == 200
    assert "Demo account" in r.text
    assert "Use demo code" in r.text
    code_match = re.search(r'name="code"\s+value="(\d{6})"', r.text)
    assert code_match, "Hidden demo code input not found"
    assert pyotp.TOTP(STAFF_TOTP_SECRET).verify(code_match.group(1), valid_window=2)


def test_mfa_verify_demo_hint_absent_when_demo_mode_false(demo_client: TestClient):
    """DEMO_MODE=false → no demo hint on /mfa/verify even for demo accounts."""
    _login_password_step(demo_client, ADMIN_EMAIL, ADMIN_PASSWORD)
    with patch("app.routers.auth.get_settings") as mock_settings:
        mock_settings.return_value.DEMO_MODE = False
        r = demo_client.get("/mfa/verify")
    assert r.status_code == 200
    assert "Demo account" not in r.text
    assert "Use demo code" not in r.text


def test_mfa_verify_demo_hint_absent_for_other_users(demo_client: TestClient, demo_db: Session):
    """DEMO_MODE=true but non-demo user → no demo hint on /mfa/verify."""
    _add_user(demo_db, "other@example.com", "Other User", "OtherPass1!", "JBSWY3DPEHPK3PXR", "Staff")
    demo_db.commit()

    _login_password_step(demo_client, "other@example.com", "OtherPass1!")
    with patch("app.routers.auth.get_settings") as mock_settings:
        mock_settings.return_value.DEMO_MODE = True
        r = demo_client.get("/mfa/verify")
    assert r.status_code == 200
    assert "Demo account" not in r.text
    assert "Use demo code" not in r.text


# ---------------------------------------------------------------------------
# 3. newstaff@onyx.demo — no TOTP → QR setup page on first sign-in
# ---------------------------------------------------------------------------


def test_newstaff_has_no_totp_and_goes_to_mfa_setup(demo_client: TestClient):
    """newstaff@onyx.demo has mfa_enabled=False → login redirects to /mfa/setup."""
    r1 = demo_client.get("/login")
    csrf = _csrf(r1)
    r2 = demo_client.post(
        "/login",
        data={"email": NEWSTAFF_EMAIL, "password": NEWSTAFF_PASSWORD, "csrf_token": csrf},
        follow_redirects=False,
    )
    assert r2.status_code == 303
    assert "/mfa/setup" in r2.headers.get("location", ""), (
        f"Expected /mfa/setup, got: {r2.headers.get('location')}"
    )


def test_newstaff_mfa_setup_shows_qr(demo_client: TestClient):
    """After newstaff password, GET /mfa/setup returns 200 with QR code."""
    r1 = demo_client.get("/login")
    csrf = _csrf(r1)
    demo_client.post(
        "/login",
        data={"email": NEWSTAFF_EMAIL, "password": NEWSTAFF_PASSWORD, "csrf_token": csrf},
        follow_redirects=False,
    )
    r3 = demo_client.get("/mfa/setup")
    assert r3.status_code == 200
    assert "data:image/png;base64," in r3.text


def test_newstaff_constants_exported_from_reset_db():
    """NEWSTAFF_* constants are importable from scripts.reset_db."""
    from scripts.reset_db import NEWSTAFF_EMAIL, NEWSTAFF_PASSWORD, NEWSTAFF_DISPLAY_NAME
    assert NEWSTAFF_EMAIL == "newstaff@onyx.demo"
    assert NEWSTAFF_PASSWORD == "OnyxNew2026!"
    assert NEWSTAFF_DISPLAY_NAME == "New Staff"
