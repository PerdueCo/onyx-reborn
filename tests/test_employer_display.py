"""tests/test_employer_display.py — employer list display fixes.

Tests:
  1. Demo seed does NOT create a "[Demo Seed Marker]" employer.
  2. Employer list page (/employment?tab=employers) never renders literal
     "&lt;span" text (escaped-HTML regression check).
  3. Employer list page (/employment/employers) never renders literal
     "&lt;span" text (regression check for the standalone list page).
  4. An employer with blank optional fields shows a "—" dash character,
     NOT escaped HTML, on the overview employers tab.
  5. An employer with blank optional fields shows a "—" dash character on
     the standalone employers list page.
  6. Inactive employers are hidden from both employer pages.
"""
from __future__ import annotations

import re

import pyotp
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app as fastapi_app
from app.models import Employer, LocalCredential, Role, UserAccount, UserRole
from app.security import encrypt_totp_secret, hash_password

# ---------------------------------------------------------------------------
# Shared test credentials
# ---------------------------------------------------------------------------

_EMAIL = "etest@onyx.test"
_PASSWORD = "OnyxTest2026!"
_TOTP = "JBSWY3DPEHPK3PXP"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def edb(db_session: Session) -> Session:
    """Seed roles + admin user for employment tests."""
    from scripts.seed_roles import seed as seed_roles

    seed_roles(db_session)

    user = UserAccount(
        provider="local",
        provider_subject=_EMAIL,
        display_name="Emp Test Admin",
        email=_EMAIL,
        active=True,
    )
    db_session.add(user)
    db_session.flush()

    cred = LocalCredential(
        user_account_id=user.id,
        password_hash=hash_password(_PASSWORD),
        totp_secret_encrypted=encrypt_totp_secret(_TOTP),
        mfa_enabled=True,
        recovery_codes_hash=[],
        failed_logins=0,
    )
    db_session.add(cred)

    role = db_session.query(Role).filter_by(name="Administrator").first()
    if role:
        db_session.add(UserRole(user_account_id=user.id, role_id=role.id))
    db_session.commit()
    return db_session


@pytest.fixture()
def eclient(edb: Session) -> TestClient:
    """Pre-authenticated TestClient backed by the seeded in-memory DB."""
    from app.db import get_db

    def _override():
        yield edb

    fastapi_app.dependency_overrides[get_db] = _override
    with TestClient(fastapi_app, raise_server_exceptions=True) as c:
        _login(c)
        yield c
    fastapi_app.dependency_overrides.clear()


def _login(client: TestClient) -> None:
    r1 = client.get("/login")
    csrf = re.search(r'name="csrf_token"\s+value="([^"]+)"', r1.text).group(1)
    r2 = client.post(
        "/login",
        data={"email": _EMAIL, "password": _PASSWORD, "csrf_token": csrf},
        follow_redirects=False,
    )
    assert r2.status_code == 303
    r3 = client.get("/mfa/verify")
    csrf2 = re.search(r'name="csrf_token"\s+value="([^"]+)"', r3.text).group(1)
    code = pyotp.TOTP(_TOTP).now()
    r4 = client.post(
        "/mfa/verify",
        data={"code": code, "csrf_token": csrf2},
        follow_redirects=False,
    )
    assert r4.status_code == 303, f"MFA failed: {r4.text[:300]}"


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _add_employer(db: Session, **kwargs) -> Employer:
    e = Employer(**{"active": True, **kwargs})
    db.add(e)
    db.commit()
    db.refresh(e)
    return e


# ---------------------------------------------------------------------------
# 1. seed_demo never creates a Demo Seed Marker employer
# ---------------------------------------------------------------------------


def test_seed_demo_no_marker_employer(db_session: Session):
    """seed_demo.seed() must not create any employer named '[Demo Seed Marker]'."""
    from scripts.seed_roles import seed as seed_roles
    from scripts.seed_demo import seed as seed_demo

    seed_roles(db_session)
    seed_demo(db_session)

    marker = (
        db_session.query(Employer)
        .filter(Employer.name.contains("Demo Seed Marker"))
        .first()
    )
    assert marker is None, f"Marker employer still exists: {marker.name!r}"


def test_seed_demo_no_demo_seed_legacy_code(db_session: Session):
    """seed_demo.seed() must not create an employer with legacy_code='DEMO_SEED'."""
    from scripts.seed_roles import seed as seed_roles
    from scripts.seed_demo import seed as seed_demo

    seed_roles(db_session)
    seed_demo(db_session)

    marker = db_session.query(Employer).filter_by(legacy_code="DEMO_SEED").first()
    assert marker is None, "Found DEMO_SEED legacy_code employer"


# ---------------------------------------------------------------------------
# 2 & 3. No escaped HTML in employer list pages
# ---------------------------------------------------------------------------


def test_overview_employers_tab_no_escaped_span(eclient: TestClient, edb: Session):
    """Overview ?tab=employers must not contain literal '&lt;span' text."""
    _add_employer(edb, name="Blank Employer")  # city/state/phone all None
    r = eclient.get("/employment?tab=employers")
    assert r.status_code == 200
    assert "&lt;span" not in r.text, "Escaped <span> HTML found in overview employers tab"


def test_employers_list_page_no_escaped_span(eclient: TestClient, edb: Session):
    """Standalone /employment/employers page must not contain literal '&lt;span' text."""
    _add_employer(edb, name="Blank Corp")  # city/state/phone all None
    r = eclient.get("/employment/employers")
    assert r.status_code == 200
    assert "&lt;span" not in r.text, "Escaped <span> HTML found in /employment/employers"


# ---------------------------------------------------------------------------
# 4 & 5. Blank optional fields show an em-dash, not escaped HTML
# ---------------------------------------------------------------------------


def test_overview_blank_fields_show_dash(eclient: TestClient, edb: Session):
    """Overview employers tab: employer with no city/state/phone/type shows '—'."""
    _add_employer(edb, name="No Details Corp")
    r = eclient.get("/employment?tab=employers")
    assert r.status_code == 200
    assert "No Details Corp" in r.text
    # The unicode em-dash (—) must appear as a visible character, not escaped HTML
    assert "—" in r.text


def test_employers_list_blank_fields_show_dash(eclient: TestClient, edb: Session):
    """Standalone employer list: employer with no city/state/phone/type shows '—'."""
    _add_employer(edb, name="Minimal Employer")
    r = eclient.get("/employment/employers")
    assert r.status_code == 200
    assert "Minimal Employer" in r.text
    assert "—" in r.text


# ---------------------------------------------------------------------------
# 6. Inactive employers are hidden
# ---------------------------------------------------------------------------


def test_inactive_employer_hidden_from_overview(eclient: TestClient, edb: Session):
    """Inactive employer must not appear in the overview employers tab."""
    _add_employer(edb, name="Active Employer GA", city="Atlanta", state="GA")
    _add_employer(edb, name="Inactive Employer", active=False, city="Macon", state="GA")

    r = eclient.get("/employment?tab=employers")
    assert r.status_code == 200
    assert "Active Employer GA" in r.text
    assert "Inactive Employer" not in r.text


def test_inactive_employer_hidden_from_list_page(eclient: TestClient, edb: Session):
    """Inactive employer must not appear on the standalone /employment/employers page."""
    _add_employer(edb, name="Visible Employer", city="Augusta", state="GA")
    _add_employer(edb, name="Hidden Employer", active=False)

    r = eclient.get("/employment/employers")
    assert r.status_code == 200
    assert "Visible Employer" in r.text
    assert "Hidden Employer" not in r.text


def test_demo_seed_marker_not_in_employer_page(eclient: TestClient, edb: Session):
    """Employer pages must never show '(Demo Seed Marker)' text regardless of DB state."""
    # Even if someone manually inserted a legacy marker row, it should be inactive
    # and therefore hidden.  This test inserts such a row as inactive and confirms.
    ghost = Employer(name="[Demo Seed Marker]", legacy_code="DEMO_SEED", active=False)
    edb.add(ghost)
    edb.commit()

    r = eclient.get("/employment?tab=employers")
    assert "Demo Seed Marker" not in r.text, "Marker employer visible in overview"

    r2 = eclient.get("/employment/employers")
    assert "Demo Seed Marker" not in r2.text, "Marker employer visible in list page"
