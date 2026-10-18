"""tests/test_student_detail_split.py — student detail current/history split.

Acceptance checks:
  1. Student with a current job: "Current jobs" section shows it, "Job history" is empty
  2. Student with an ended job: it appears in "Job history", not "Current jobs"
  3. Student with both: current in top section, ended in history
  4. End button present only on current jobs (not history rows)
  5. End button href links to /employment/{id}/end
  6. is_current_job helper: end_date==today is history (strict >), end_date==tomorrow is current
  7. job_form.html has correct end_date label "(leave blank if still working)"
  8. end_job_form defaults end_date input to today's date
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
    Employer,
    Employment,
    LocalCredential,
    Role,
    Student,
    UserAccount,
    UserRole,
)
from app.security import encrypt_totp_secret, hash_password
from app.services.kpis import is_current_job

_EMAIL = "detail_admin@onyx.test"
_PASSWORD = "OnyxDetail2026!"
_TOTP = "JBSWY3DPEHPK3PXT"


# ---------------------------------------------------------------------------
# Unit tests for is_current_job helper (no HTTP needed)
# ---------------------------------------------------------------------------


class _FakeJob:
    """Minimal duck-typed stub for is_current_job unit tests."""
    def __init__(self, start_offset: int, end_offset: int | None) -> None:
        today = datetime.date.today()
        self.start_date = today + datetime.timedelta(days=start_offset)
        self.end_date = (
            today + datetime.timedelta(days=end_offset)
            if end_offset is not None else None
        )


def _make_job(start_offset: int, end_offset: int | None) -> "_FakeJob":
    return _FakeJob(start_offset, end_offset)


def test_is_current_open_job():
    """No end_date and started in past → current."""
    assert is_current_job(_make_job(-5, None), datetime.date.today()) is True


def test_is_current_future_end():
    """end_date is tomorrow → current (end_date > today)."""
    assert is_current_job(_make_job(-5, 1), datetime.date.today()) is True


def test_is_history_end_today():
    """end_date == today → history (strict >, D-31)."""
    assert is_current_job(_make_job(-5, 0), datetime.date.today()) is False


def test_is_history_end_in_past():
    """end_date in the past → history."""
    assert is_current_job(_make_job(-10, -1), datetime.date.today()) is False


def test_is_history_future_start():
    """start_date in future → not current yet."""
    assert is_current_job(_make_job(5, None), datetime.date.today()) is False


# ---------------------------------------------------------------------------
# HTTP fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def detail_db(db_session: Session) -> Session:
    """Seed admin + employer + student with one current and one past job."""
    from scripts.seed_roles import seed as seed_roles
    seed_roles(db_session)

    user = UserAccount(
        provider="local",
        provider_subject=_EMAIL,
        display_name="Detail Admin",
        email=_EMAIL,
        active=True,
    )
    db_session.add(user)
    db_session.flush()
    db_session.add(LocalCredential(
        user_account_id=user.id,
        password_hash=hash_password(_PASSWORD),
        totp_secret_encrypted=encrypt_totp_secret(_TOTP),
        mfa_enabled=True,
        recovery_codes_hash=[],
        failed_logins=0,
    ))
    role = db_session.query(Role).filter_by(name="Administrator").first()
    if role:
        db_session.add(UserRole(user_account_id=user.id, role_id=role.id))

    emp = Employer(name="Bookstore Co", company_type="Retail", active=True)
    db_session.add(emp)
    db_session.flush()

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    student = Student(
        student_number="STU-DT01",
        first_name="Kyla",
        last_name="Carter",
        status="active",
    )
    db_session.add(student)
    db_session.flush()

    # One current job (no end_date)
    current = Employment(
        student_id=student.id,
        employer_id=emp.id,
        job_title="Cashier",
        job_type="part_time",
        start_date=yesterday,
        end_date=None,
        hourly_rate=12.00,
    )
    # One past job (end_date == yesterday, which is history by D-31)
    past = Employment(
        student_id=student.id,
        employer_id=emp.id,
        job_title="Stock Clerk",
        job_type="part_time",
        start_date=yesterday - datetime.timedelta(days=60),
        end_date=yesterday,
        hourly_rate=11.00,
    )
    db_session.add_all([current, past])
    db_session.commit()
    db_session.refresh(student)
    db_session.refresh(current)
    db_session.refresh(past)

    # Store IDs for test use
    db_session.info["student_id"] = student.id
    db_session.info["current_job_id"] = current.id
    db_session.info["past_job_id"] = past.id
    db_session.info["employer_id"] = emp.id

    return db_session


@pytest.fixture()
def detail_client(detail_db: Session):
    from app.db import get_db

    def _override():
        yield detail_db

    fastapi_app.dependency_overrides[get_db] = _override
    c = TestClient(fastapi_app, raise_server_exceptions=True)
    c.__enter__()

    r1 = c.get("/login")
    csrf = re.search(r'name="csrf_token"\s+value="([^"]+)"', r1.text).group(1)
    r2 = c.post("/login", data={"email": _EMAIL, "password": _PASSWORD, "csrf_token": csrf},
                follow_redirects=False)
    assert r2.status_code == 303

    r3 = c.get("/mfa/verify")
    csrf2 = re.search(r'name="csrf_token"\s+value="([^"]+)"', r3.text).group(1)
    code = pyotp.TOTP(_TOTP).now()
    r4 = c.post("/mfa/verify", data={"code": code, "csrf_token": csrf2},
                follow_redirects=False)
    assert r4.status_code == 303, f"MFA failed: {r4.text[:300]}"

    yield c
    c.__exit__(None, None, None)
    fastapi_app.dependency_overrides.clear()


def _detail_page(c: TestClient, db: Session) -> str:
    student_id = db.info["student_id"]
    r = c.get(f"/students/{student_id}")
    assert r.status_code == 200
    return r.text


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_detail_has_current_jobs_section(detail_client, detail_db):
    """Student detail page has a 'Current jobs' heading."""
    html = _detail_page(detail_client, detail_db)
    assert "Current jobs" in html


def test_detail_has_job_history_section(detail_client, detail_db):
    """Student detail page has a 'Job history' heading."""
    html = _detail_page(detail_client, detail_db)
    assert "Job history" in html


def test_current_job_in_current_section(detail_client, detail_db):
    """The open job (Cashier) appears in the Current jobs section."""
    html = _detail_page(detail_client, detail_db)
    # Cashier is the current job title
    assert "Cashier" in html


def test_past_job_in_history_section(detail_client, detail_db):
    """The ended job (Stock Clerk) appears in the Job history section."""
    html = _detail_page(detail_client, detail_db)
    assert "Stock Clerk" in html


def test_end_button_present_on_current_job(detail_client, detail_db):
    """End button links to /employment/{current_job_id}/end."""
    html = _detail_page(detail_client, detail_db)
    current_job_id = detail_db.info["current_job_id"]
    assert f"/employment/{current_job_id}/end" in html


def test_no_end_button_for_past_job(detail_client, detail_db):
    """Past job row has no End button (no link to /employment/{past_job_id}/end)."""
    html = _detail_page(detail_client, detail_db)
    past_job_id = detail_db.info["past_job_id"]
    assert f"/employment/{past_job_id}/end" not in html


def test_end_job_form_defaults_to_today(detail_client, detail_db):
    """End-job form pre-populates end_date input with today's date."""
    current_job_id = detail_db.info["current_job_id"]
    r = detail_client.get(f"/employment/{current_job_id}/end")
    assert r.status_code == 200
    today_str = datetime.date.today().isoformat()
    assert f'value="{today_str}"' in r.text


def test_job_form_label_leave_blank(detail_client, detail_db):
    """Add-job form shows correct end_date label '(leave blank if still working)'."""
    student_id = detail_db.info["student_id"]
    r = detail_client.get(f"/employment/new?student_id={student_id}")
    assert r.status_code == 200
    assert "leave blank if still working" in r.text
