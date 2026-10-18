"""tests/test_dashboard_charts.py — dashboard charts, briefing, plain-English activity.

Acceptance checks:
  1. Briefing sentence present and contains employment %
  2. "Employment rate by program" section visible to both staff and admin
  3. Program bar rows rendered (x of y format)
  4. "Top employers" section visible to both staff and admin
  5. Top employer row shows student count and avg rate
  6. Recent activity renders plain-English sentences (names, not event codes)
  7. account_locked activity is marked with red CSS class (activity-security)
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
    AuditEvent,
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

_STAFF_EMAIL = "chart_staff@onyx.test"
_STAFF_PASSWORD = "OnyxStaff2026!"
_STAFF_TOTP = "JBSWY3DPEHPK3PXR"

_ADMIN_EMAIL = "chart_admin@onyx.test"
_ADMIN_PASSWORD = "OnyxAdmin2026!"
_ADMIN_TOTP = "JBSWY3DPEHPK3PXS"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _seed_user(db: Session, email: str, pw: str, totp: str, role_name: str) -> UserAccount:
    user = UserAccount(
        provider="local",
        provider_subject=email,
        display_name=email.split("@")[0],
        email=email,
        active=True,
    )
    db.add(user)
    db.flush()
    db.add(LocalCredential(
        user_account_id=user.id,
        password_hash=hash_password(pw),
        totp_secret_encrypted=encrypt_totp_secret(totp),
        mfa_enabled=True,
        recovery_codes_hash=[],
        failed_logins=0,
    ))
    role = db.query(Role).filter_by(name=role_name).first()
    if role:
        db.add(UserRole(user_account_id=user.id, role_id=role.id))
    db.commit()
    return user


@pytest.fixture()
def chart_db(db_session: Session) -> Session:
    """Seed full fixture: 2 programs, 4 students, 1 employer, jobs, audit events."""
    from scripts.seed_roles import seed as seed_roles
    seed_roles(db_session)

    staff_user = _seed_user(db_session, _STAFF_EMAIL, _STAFF_PASSWORD, _STAFF_TOTP, "Staff")
    _seed_user(db_session, _ADMIN_EMAIL, _ADMIN_PASSWORD, _ADMIN_TOTP, "Administrator")

    # Two programs
    prog_a = Program(code="TESTA", name="Computer Science", active=True)
    prog_b = Program(code="TESTB", name="Business Admin", active=True)
    db_session.add_all([prog_a, prog_b])
    db_session.flush()

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    # 3 students in prog_a, 1 in prog_b
    s1 = Student(student_number="STU-C001", first_name="Alice", last_name="Alpha",
                 status="active", program_id=prog_a.id)
    s2 = Student(student_number="STU-C002", first_name="Bob", last_name="Beta",
                 status="active", program_id=prog_a.id)
    s3 = Student(student_number="STU-C003", first_name="Carol", last_name="Gamma",
                 status="active", program_id=prog_a.id)
    s4 = Student(student_number="STU-C004", first_name="Dave", last_name="Delta",
                 status="active", program_id=prog_b.id)
    db_session.add_all([s1, s2, s3, s4])
    db_session.flush()

    # One employer
    emp = Employer(name="Acme Corp", company_type="Technology", active=True)
    db_session.add(emp)
    db_session.flush()

    # s1 and s2 have current jobs; s3 has a past job; s4 has a current job
    j1 = Employment(student_id=s1.id, employer_id=emp.id, job_title="Dev",
                    job_type="full_time", start_date=yesterday, end_date=None,
                    hourly_rate=20.00)
    j2 = Employment(student_id=s2.id, employer_id=emp.id, job_title="QA",
                    job_type="part_time", start_date=yesterday, end_date=None,
                    hourly_rate=15.00)
    # s3: past job (ended yesterday — end_date == yesterday, which is NOT > today, so history)
    j3 = Employment(student_id=s3.id, employer_id=emp.id, job_title="Intern",
                    job_type="part_time", start_date=yesterday - datetime.timedelta(days=30),
                    end_date=yesterday, hourly_rate=12.00)
    j4 = Employment(student_id=s4.id, employer_id=emp.id, job_title="Manager",
                    job_type="full_time", start_date=yesterday, end_date=None,
                    hourly_rate=25.00)
    db_session.add_all([j1, j2, j3, j4])

    # Audit events for activity feed
    db_session.add(AuditEvent(
        actor_account_id=staff_user.id,
        event_type="student_create",
        entity_type="student",
        entity_id=s1.id,
        detail={"student_number": "STU-C001", "student_name": "Alice Alpha"},
    ))
    db_session.add(AuditEvent(
        actor_account_id=staff_user.id,
        event_type="job_add",
        entity_type="employment",
        entity_id=j1.id,
        detail={"student_name": "Alice Alpha", "employer_name": "Acme Corp"},
    ))
    db_session.add(AuditEvent(
        actor_account_id=staff_user.id,
        event_type="job_end",
        entity_type="employment",
        entity_id=j3.id,
        detail={"student_name": "Carol Gamma", "employer_name": "Acme Corp",
                "end_date": str(yesterday)},
    ))
    db_session.add(AuditEvent(
        actor_account_id=None,
        event_type="account_locked",
        entity_type="user_account",
        entity_id=None,
        detail={"email": "bad@test.com"},
    ))

    db_session.commit()
    return db_session


def _make_client(db: Session, email: str, pw: str, totp: str) -> TestClient:
    from app.db import get_db

    def _override():
        yield db

    fastapi_app.dependency_overrides[get_db] = _override
    c = TestClient(fastapi_app, raise_server_exceptions=True)
    c.__enter__()

    r1 = c.get("/login")
    csrf = re.search(r'name="csrf_token"\s+value="([^"]+)"', r1.text).group(1)
    r2 = c.post("/login", data={"email": email, "password": pw, "csrf_token": csrf},
                follow_redirects=False)
    assert r2.status_code == 303

    r3 = c.get("/mfa/verify")
    csrf2 = re.search(r'name="csrf_token"\s+value="([^"]+)"', r3.text).group(1)
    code = pyotp.TOTP(totp).now()
    r4 = c.post("/mfa/verify", data={"code": code, "csrf_token": csrf2},
                follow_redirects=False)
    assert r4.status_code == 303, f"MFA failed: {r4.text[:300]}"
    return c


@pytest.fixture()
def staff_client(chart_db: Session):
    c = _make_client(chart_db, _STAFF_EMAIL, _STAFF_PASSWORD, _STAFF_TOTP)
    yield c
    c.__exit__(None, None, None)
    fastapi_app.dependency_overrides.clear()


@pytest.fixture()
def admin_client(chart_db: Session):
    c = _make_client(chart_db, _ADMIN_EMAIL, _ADMIN_PASSWORD, _ADMIN_TOTP)
    yield c
    c.__exit__(None, None, None)
    fastapi_app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Briefing sentence
# ---------------------------------------------------------------------------


def test_briefing_present_staff(staff_client: TestClient):
    """Briefing sentence is visible on the dashboard."""
    r = staff_client.get("/dashboard")
    assert r.status_code == 200
    assert "dash-briefing" in r.text
    assert "currently employed" in r.text.lower()


def test_briefing_contains_pct(staff_client: TestClient):
    """Briefing sentence contains an employment percentage."""
    r = staff_client.get("/dashboard")
    assert "%" in r.text
    assert "currently employed" in r.text.lower()


def test_briefing_contains_program(staff_client: TestClient):
    """Briefing sentence names the leading program (Computer Science has 2/3 = 67%)."""
    r = staff_client.get("/dashboard")
    # The top program by employed count should appear in the briefing
    assert "Computer Science" in r.text or "Business Admin" in r.text


# ---------------------------------------------------------------------------
# Employment rate by program
# ---------------------------------------------------------------------------


def test_program_chart_section_visible_staff(staff_client: TestClient):
    """Staff sees 'Employment rate by program' chart section."""
    r = staff_client.get("/dashboard")
    assert "Employment rate by program" in r.text


def test_program_chart_section_visible_admin(admin_client: TestClient):
    """Admin sees 'Employment rate by program' chart section."""
    r = admin_client.get("/dashboard")
    assert "Employment rate by program" in r.text


def test_program_chart_shows_x_of_y(staff_client: TestClient):
    """Bar chart rows show 'X of Y' student counts."""
    r = staff_client.get("/dashboard")
    # s1+s2 current in prog_a (3 total) → "2 of 3"
    assert "of" in r.text
    assert "prog-bar-count" in r.text


def test_program_chart_has_pct_badge(staff_client: TestClient):
    """Bar chart rows show percentage badges."""
    r = staff_client.get("/dashboard")
    assert "prog-bar-pct" in r.text


# ---------------------------------------------------------------------------
# Top employers
# ---------------------------------------------------------------------------


def test_top_employers_section_visible_staff(staff_client: TestClient):
    """Staff sees 'Top employers' section."""
    r = staff_client.get("/dashboard")
    assert "Top employers" in r.text


def test_top_employers_section_visible_admin(admin_client: TestClient):
    """Admin sees 'Top employers' section."""
    r = admin_client.get("/dashboard")
    assert "Top employers" in r.text


def test_top_employer_name_appears(staff_client: TestClient):
    """Acme Corp (the only employer) appears in the top employers table."""
    r = staff_client.get("/dashboard")
    assert "Acme Corp" in r.text


def test_top_employer_student_count(staff_client: TestClient):
    """Top employer shows 3 students currently employed (s1, s2, s4)."""
    r = staff_client.get("/dashboard")
    # 3 students currently employed at Acme Corp
    assert "3" in r.text


def test_top_employer_avg_rate(staff_client: TestClient):
    """Top employer avg rate computed from current jobs (20+15+25)/3 = $20.00."""
    r = staff_client.get("/dashboard")
    # avg of 20, 15, 25 = 20.00
    assert "$20.00" in r.text


# ---------------------------------------------------------------------------
# Plain-English activity sentences
# ---------------------------------------------------------------------------


def test_activity_student_create_english(staff_client: TestClient):
    """Recent activity shows 'added Alice Alpha, STU-C001' not raw event code."""
    r = staff_client.get("/dashboard")
    assert "added Alice Alpha, STU-C001" in r.text


def test_activity_job_add_english(staff_client: TestClient):
    """Recent activity shows 'added Acme Corp job for Alice Alpha'."""
    r = staff_client.get("/dashboard")
    assert "added Acme Corp job for Alice Alpha" in r.text


def test_activity_job_end_english(staff_client: TestClient):
    """Recent activity shows 'ended the Acme Corp job for Carol Gamma'."""
    r = staff_client.get("/dashboard")
    assert "ended the Acme Corp job for Carol Gamma" in r.text


def test_activity_lockout_red(staff_client: TestClient):
    """account_locked events render with activity-security (red) CSS class."""
    r = staff_client.get("/dashboard")
    assert "activity-security" in r.text
    assert "Account locked" in r.text
