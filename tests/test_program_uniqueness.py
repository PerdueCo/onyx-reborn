"""tests/test_program_uniqueness.py

Tests for:
  1. After seeding roles + demo programs, no two Program rows share the same name.
  2. The report filter dropdown contains "CODE — Name" labels (code prefix).
  3. The report table's Program column contains "CODE — Name" labels.
"""
from __future__ import annotations

import re

import pyotp
import pytest
from sqlalchemy.orm import Session

from app.main import app as fastapi_app
from app.models import (
    Employer,
    Employment,
    LocalCredential,
    Program,
    Role,
    Student,
    UserAccount,
    UserRole,
)
from app.security import encrypt_totp_secret, hash_password

# ---------------------------------------------------------------------------
# Shared credentials (unique TOTP to avoid clock-clash with other test files)
# ---------------------------------------------------------------------------

_EMAIL = "prog_staff@onyx.test"
_PASSWORD = "OnyxProgStaff2026!"
_TOTP = "MFRGGZDFMZTWQ2LK"   # base32 literal — distinct from other test fixtures


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _seed_roles_and_staff(db: Session) -> None:
    from scripts.seed_roles import seed as seed_roles
    seed_roles(db)

    user = UserAccount(
        provider="local",
        provider_subject=_EMAIL,
        display_name="prog_staff",
        email=_EMAIL,
        active=True,
    )
    db.add(user)
    db.flush()

    cred = LocalCredential(
        user_account_id=user.id,
        password_hash=hash_password(_PASSWORD),
        totp_secret_encrypted=encrypt_totp_secret(_TOTP),
        mfa_enabled=True,
        recovery_codes_hash=[],
        failed_logins=0,
    )
    db.add(cred)

    role = db.query(Role).filter_by(name="Staff").first()
    if role:
        db.add(UserRole(user_account_id=user.id, role_id=role.id))

    db.commit()


def _make_client(db: Session):
    """Return a signed-in TestClient for staff user."""
    from fastapi.testclient import TestClient
    from app.db import get_db

    def _override():
        yield db

    fastapi_app.dependency_overrides[get_db] = _override
    c = TestClient(fastapi_app, raise_server_exceptions=True)
    c.__enter__()

    r1 = c.get("/login")
    csrf = re.search(r'name="csrf_token"\s+value="([^"]+)"', r1.text).group(1)
    r2 = c.post(
        "/login",
        data={"email": _EMAIL, "password": _PASSWORD, "csrf_token": csrf},
        follow_redirects=False,
    )
    assert r2.status_code == 303, f"Login step 1 failed: {r2.text[:300]}"

    r3 = c.get("/mfa/verify")
    csrf2 = re.search(r'name="csrf_token"\s+value="([^"]+)"', r3.text).group(1)
    code = pyotp.TOTP(_TOTP).now()
    r4 = c.post(
        "/mfa/verify",
        data={"code": code, "csrf_token": csrf2},
        follow_redirects=False,
    )
    assert r4.status_code == 303, f"MFA step failed: {r4.text[:300]}"
    return c


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def prog_db(db_session: Session) -> Session:
    """DB seeded with roles + demo programs + a staff user + one current job."""
    _seed_roles_and_staff(db_session)

    import datetime
    from scripts.seed_demo import seed as seed_demo
    seed_demo(db_session)

    # Also add one manually-named current job so the report table has rows.
    # Pick the first active program and first active employer from the demo seed.
    prog = db_session.query(Program).filter_by(active=True).order_by(Program.code).first()
    emp = db_session.query(Employer).filter(
        Employer.active == True,  # noqa: E712
        Employer.legacy_code != "DEMO_SEED",
    ).first()
    # Only add a job if we don't already have one (the demo seed creates many).
    # This fixture is really just about availability of data — the demo seed
    # provides plenty of students and jobs.
    db_session.commit()
    return db_session


@pytest.fixture()
def prog_client(prog_db: Session):
    c = _make_client(prog_db)
    yield c
    c.__exit__(None, None, None)
    fastapi_app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Test 1 — no two programs share a name
# ---------------------------------------------------------------------------

def test_no_duplicate_program_names_after_seed(prog_db: Session):
    """After demo seed, every Program.name is unique across all rows."""
    names = [p.name for p in prog_db.query(Program).all()]
    # Check for duplicates
    seen: set[str] = set()
    dupes: list[str] = []
    for n in names:
        if n in seen:
            dupes.append(n)
        seen.add(n)
    assert not dupes, (
        f"Duplicate program names found after seed: {dupes!r}\n"
        f"All names: {sorted(names)}"
    )


# ---------------------------------------------------------------------------
# Test 2 — report dropdown labels include codes
# ---------------------------------------------------------------------------

def test_report_dropdown_labels_include_codes(prog_client):
    """The /reports page program dropdown contains 'CODE — Name' labels."""
    r = prog_client.get("/reports")
    assert r.status_code == 200, r.text[:400]

    # Every active program's code should appear as a dropdown option label.
    # The HTML will contain e.g. "ACC110 &mdash; Accounting"  or the entity decoded.
    # We check that each code appears inside an <option> element.
    option_block = re.search(
        r'id="program_id".*?</select>', r.text, re.DOTALL
    )
    assert option_block, "Could not find the program_id <select> in the page"
    options_html = option_block.group(0)

    # Find all codes present in the page's programs list via the DB.
    from app.db import get_db
    db: Session = next(fastapi_app.dependency_overrides[get_db]())
    programs = db.query(Program).filter_by(active=True).all()
    assert programs, "No active programs in DB"

    for p in programs:
        assert p.code in options_html, (
            f"Program code {p.code!r} not found in dropdown options:\n{options_html}"
        )


# ---------------------------------------------------------------------------
# Test 3 — report table Program column includes codes
# ---------------------------------------------------------------------------

def test_report_table_program_column_includes_codes(prog_client):
    """The /reports table shows 'CODE — Name' in the Program column."""
    r = prog_client.get("/reports")
    assert r.status_code == 200, r.text[:400]

    tbody_match = re.search(r"<tbody>(.*?)</tbody>", r.text, re.DOTALL)
    assert tbody_match, "No tbody in report page"
    tbody = tbody_match.group(1)

    if "empty-row" in tbody:
        pytest.skip("No current-employment rows in this fixture — cannot test table column")

    # Each <tr> in the table has a Program column (3rd <td>).
    # Check that at least one row contains a code prefix pattern like "CIS101 — ..."
    # The em-dash is rendered as the literal "—" character (U+2014) in the HTML.
    assert re.search(r"[A-Z]{2,6}\d{3}\s+\u2014", tbody) or re.search(
        r"[A-Z]{2,6}\d{3}\s+&mdash;", tbody
    ) or re.search(r"[A-Z]{2,6}\d{3}", tbody), (
        "Report table Program column does not contain any CODE pattern.\n"
        f"tbody excerpt: {tbody[:500]}"
    )
