"""tests/test_reports.py — Current Employment report tests.

Acceptance checks (run-sheet step 8):
  1. /reports loads (200) for a user with reports.read.
  2. HTML table has all 7 expected column headers.
  3. Only current jobs appear (ended jobs are excluded).
  4. Filter by employer: HTML row count matches CSV row count for that filter.
  5. Filter by program: HTML row count matches CSV row count for that filter.
  6. CSV headers match the on-screen table headers exactly.
  7. Unauthenticated request → 303 redirect to /login.
  8. Empty filter result shows 0 records found.
"""
from __future__ import annotations

import csv
import datetime
import io
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
    Program,
    Role,
    Student,
    UserAccount,
    UserRole,
)
from app.security import encrypt_totp_secret, hash_password

# ---------------------------------------------------------------------------
# Shared credentials
# ---------------------------------------------------------------------------

_STAFF_EMAIL = "rep_staff@onyx.test"
_STAFF_PASSWORD = "OnyxRepStaff2026!"
_STAFF_TOTP = "JBSWY3DPEHPK3PXR"   # distinct to avoid clock clash with other tests


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _seed_staff(db: Session) -> UserAccount:
    user = UserAccount(
        provider="local",
        provider_subject=_STAFF_EMAIL,
        display_name="rep_staff",
        email=_STAFF_EMAIL,
        active=True,
    )
    db.add(user)
    db.flush()

    cred = LocalCredential(
        user_account_id=user.id,
        password_hash=hash_password(_STAFF_PASSWORD),
        totp_secret_encrypted=encrypt_totp_secret(_STAFF_TOTP),
        mfa_enabled=True,
        recovery_codes_hash=[],
        failed_logins=0,
    )
    db.add(cred)

    role = db.query(Role).filter_by(name="Staff").first()
    if role:
        db.add(UserRole(user_account_id=user.id, role_id=role.id))

    db.commit()
    return user


@pytest.fixture()
def rep_db(db_session: Session) -> Session:
    """Seed roles + fixture data for report tests.

    Fixture:
      - 2 programs: Alpha, Beta
      - 2 employers: Corp A, Corp B
      - 3 students (all active):
          * s1 → Alpha, current job at Corp A (no end_date)
          * s2 → Beta,  current job at Corp B (no end_date)
          * s3 → Alpha, ended job at Corp A (end_date = yesterday — excluded)
    """
    from scripts.seed_roles import seed as seed_roles
    seed_roles(db_session)
    _seed_staff(db_session)

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    prog_a = Program(code="ALPHA", name="Alpha Program", active=True)
    prog_b = Program(code="BETA", name="Beta Program", active=True)
    db_session.add_all([prog_a, prog_b])
    db_session.flush()

    emp_a = Employer(name="Corp A", active=True)
    emp_b = Employer(name="Corp B", active=True)
    db_session.add_all([emp_a, emp_b])
    db_session.flush()

    s1 = Student(student_number="STU-R001", first_name="Alice", last_name="Anderson",
                 status="active", program_id=prog_a.id)
    s2 = Student(student_number="STU-R002", first_name="Bob", last_name="Brown",
                 status="active", program_id=prog_b.id)
    s3 = Student(student_number="STU-R003", first_name="Carol", last_name="Clark",
                 status="active", program_id=prog_a.id)
    db_session.add_all([s1, s2, s3])
    db_session.flush()

    # s1 current job at Corp A
    db_session.add(Employment(
        student_id=s1.id, employer_id=emp_a.id,
        job_title="Analyst", job_type="full_time",
        start_date=today - datetime.timedelta(days=30),
        end_date=None,
        hours_per_week=40,
        hourly_rate="18.00",
    ))
    # s2 current job at Corp B
    db_session.add(Employment(
        student_id=s2.id, employer_id=emp_b.id,
        job_title="Technician", job_type="part_time",
        start_date=today - datetime.timedelta(days=10),
        end_date=None,
        hours_per_week=20,
        hourly_rate="14.50",
    ))
    # s3 ended job at Corp A — should be EXCLUDED from current employment
    db_session.add(Employment(
        student_id=s3.id, employer_id=emp_a.id,
        job_title="Intern", job_type="part_time",
        start_date=today - datetime.timedelta(days=60),
        end_date=yesterday,
        hours_per_week=15,
        hourly_rate="12.00",
    ))

    db_session.commit()
    return db_session


def _make_client(db: Session) -> TestClient:
    """Return a signed-in TestClient overriding the DB with *db*."""
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
        data={"email": _STAFF_EMAIL, "password": _STAFF_PASSWORD, "csrf_token": csrf},
        follow_redirects=False,
    )
    assert r2.status_code == 303, f"Login failed: {r2.text[:300]}"

    r3 = c.get("/mfa/verify")
    csrf2 = re.search(r'name="csrf_token"\s+value="([^"]+)"', r3.text).group(1)
    code = pyotp.TOTP(_STAFF_TOTP).now()
    r4 = c.post(
        "/mfa/verify",
        data={"code": code, "csrf_token": csrf2},
        follow_redirects=False,
    )
    assert r4.status_code == 303, f"MFA failed: {r4.text[:300]}"
    return c


@pytest.fixture()
def staff_client(rep_db: Session):
    c = _make_client(rep_db)
    yield c
    c.__exit__(None, None, None)
    fastapi_app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Helper: count data rows in HTML table (tbody <tr>s, excluding empty-row)
# ---------------------------------------------------------------------------

def _html_row_count(html: str) -> int:
    """Count <tr> elements inside <tbody> that are real data rows."""
    tbody_match = re.search(r"<tbody>(.*?)</tbody>", html, re.DOTALL)
    if not tbody_match:
        return 0
    tbody = tbody_match.group(1)
    rows = re.findall(r"<tr>", tbody)
    # If there is an empty-row td, that means 0 data rows
    if "empty-row" in tbody:
        return 0
    return len(rows)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_reports_page_loads(staff_client: TestClient):
    """/reports → 200 for a user with reports.read."""
    r = staff_client.get("/reports")
    assert r.status_code == 200, r.text[:400]


def test_reports_html_has_column_headers(staff_client: TestClient):
    """All 7 column headers are present in the HTML table."""
    r = staff_client.get("/reports")
    for col in ["Student Name", "STU Number", "Program", "Employer",
                "Job Title", "Hours/Week", "Hourly Rate"]:
        assert col in r.text, f"Missing column header: {col}"


def test_reports_current_only(staff_client: TestClient):
    """Ended jobs are excluded; only 2 current jobs appear (not 3)."""
    r = staff_client.get("/reports")
    assert r.status_code == 200
    count = _html_row_count(r.text)
    assert count == 2, f"Expected 2 current jobs, got {count}"


def test_reports_filter_by_employer_html(staff_client: TestClient, rep_db: Session):
    """Filter by employer_id returns only rows for that employer."""
    emp_a = rep_db.query(Employer).filter_by(name="Corp A").first()
    r = staff_client.get(f"/reports?employer_id={emp_a.id}")
    assert r.status_code == 200
    count = _html_row_count(r.text)
    assert count == 1, f"Expected 1 row for Corp A, got {count}"
    assert "Anderson" in r.text    # Alice Anderson works at Corp A
    assert "Brown" not in r.text   # Bob Brown works at Corp B


def test_reports_filter_by_program_html(staff_client: TestClient, rep_db: Session):
    """Filter by program_id returns only rows for that program."""
    prog_b = rep_db.query(Program).filter_by(code="BETA").first()
    r = staff_client.get(f"/reports?program_id={prog_b.id}")
    assert r.status_code == 200
    count = _html_row_count(r.text)
    assert count == 1, f"Expected 1 row for Beta Program, got {count}"
    assert "Brown" in r.text
    assert "Anderson" not in r.text


def test_csv_headers_match_screen(staff_client: TestClient):
    """CSV first row headers match the on-screen table column names exactly."""
    r = staff_client.get("/reports/current-employment/export.csv")
    assert r.status_code == 200
    reader = csv.reader(io.StringIO(r.text))
    headers = next(reader)
    assert headers == [
        "Student Name", "STU Number", "Program",
        "Employer", "Job Title", "Hours/Week", "Hourly Rate",
    ], f"CSV headers mismatch: {headers}"


def test_csv_row_count_matches_html_unfiltered(staff_client: TestClient):
    """CSV data rows == HTML table rows when no filter is applied."""
    html_r = staff_client.get("/reports")
    csv_r = staff_client.get("/reports/current-employment/export.csv")

    html_count = _html_row_count(html_r.text)

    reader = csv.reader(io.StringIO(csv_r.text))
    next(reader)  # skip header row
    csv_count = sum(1 for _ in reader)

    assert html_count == csv_count, (
        f"HTML shows {html_count} rows but CSV has {csv_count} data rows"
    )


def test_csv_row_count_matches_html_with_employer_filter(
    staff_client: TestClient, rep_db: Session
):
    """CSV data rows == HTML table rows when filtering by employer."""
    emp_b = rep_db.query(Employer).filter_by(name="Corp B").first()
    url = f"/reports?employer_id={emp_b.id}"
    csv_url = f"/reports/current-employment/export.csv?employer_id={emp_b.id}"

    html_r = staff_client.get(url)
    csv_r = staff_client.get(csv_url)

    html_count = _html_row_count(html_r.text)

    reader = csv.reader(io.StringIO(csv_r.text))
    next(reader)
    csv_count = sum(1 for _ in reader)

    assert html_count == csv_count == 1, (
        f"Expected 1 row each; HTML={html_count}, CSV={csv_count}"
    )


def test_csv_row_count_matches_html_with_program_filter(
    staff_client: TestClient, rep_db: Session
):
    """CSV data rows == HTML table rows when filtering by program."""
    prog_a = rep_db.query(Program).filter_by(code="ALPHA").first()
    # Alpha has s1 (current) and s3 (ended) — only s1 should appear
    url = f"/reports?program_id={prog_a.id}"
    csv_url = f"/reports/current-employment/export.csv?program_id={prog_a.id}"

    html_r = staff_client.get(url)
    csv_r = staff_client.get(csv_url)

    html_count = _html_row_count(html_r.text)

    reader = csv.reader(io.StringIO(csv_r.text))
    next(reader)
    csv_count = sum(1 for _ in reader)

    assert html_count == csv_count == 1, (
        f"Expected 1 row each; HTML={html_count}, CSV={csv_count}"
    )


def test_reports_empty_filter_shows_zero(staff_client: TestClient, rep_db: Session):
    """A filter that matches no jobs shows '0 records found'."""
    # Use employer_id=9999 which doesn't exist
    r = staff_client.get("/reports?employer_id=9999")
    assert r.status_code == 200
    assert "0 records" in r.text


def test_reports_requires_auth(client):
    """/reports without a session → 303 to /login."""
    r = client.get("/reports", follow_redirects=False)
    assert r.status_code == 303
    assert "/login" in r.headers.get("location", "")


def test_csv_export_requires_auth(client):
    """/reports/current-employment/export.csv without a session → 303 to /login."""
    r = client.get("/reports/current-employment/export.csv", follow_redirects=False)
    assert r.status_code == 303
    assert "/login" in r.headers.get("location", "")


# ---------------------------------------------------------------------------
# Empty-string / mixed filter tests  (regression: FastAPI 422 on program_id="")
# ---------------------------------------------------------------------------

def test_reports_empty_string_both_params_returns_all(staff_client: TestClient):
    """?program_id=&employer_id= (the form's 'All …' selection) → 200, all 2 current rows."""
    r = staff_client.get("/reports?program_id=&employer_id=")
    assert r.status_code == 200, r.text[:400]
    count = _html_row_count(r.text)
    assert count == 2, f"Expected 2 rows with empty filters, got {count}"


def test_reports_empty_program_id_with_employer_set(staff_client: TestClient, rep_db: Session):
    """program_id= (blank) + employer_id set → filter by employer only."""
    emp_a = rep_db.query(Employer).filter_by(name="Corp A").first()
    r = staff_client.get(f"/reports?program_id=&employer_id={emp_a.id}")
    assert r.status_code == 200, r.text[:400]
    count = _html_row_count(r.text)
    assert count == 1, f"Expected 1 row (Corp A only), got {count}"
    assert "Anderson" in r.text
    assert "Brown" not in r.text


def test_reports_empty_employer_id_with_program_set(staff_client: TestClient, rep_db: Session):
    """employer_id= (blank) + program_id set → filter by program only."""
    prog_b = rep_db.query(Program).filter_by(code="BETA").first()
    r = staff_client.get(f"/reports?program_id={prog_b.id}&employer_id=")
    assert r.status_code == 200, r.text[:400]
    count = _html_row_count(r.text)
    assert count == 1, f"Expected 1 row (Beta only), got {count}"
    assert "Brown" in r.text
    assert "Anderson" not in r.text


def test_csv_export_empty_string_both_params(staff_client: TestClient):
    """CSV: ?program_id=&employer_id= → 200, 2 data rows (all current jobs)."""
    r = staff_client.get("/reports/current-employment/export.csv?program_id=&employer_id=")
    assert r.status_code == 200, r.text[:400]
    reader = csv.reader(io.StringIO(r.text))
    next(reader)  # skip header
    rows = list(reader)
    assert len(rows) == 2, f"Expected 2 CSV data rows, got {len(rows)}"


def test_csv_export_empty_program_id_with_employer_set(
    staff_client: TestClient, rep_db: Session
):
    """CSV: program_id= blank + employer_id set → 1 data row."""
    emp_b = rep_db.query(Employer).filter_by(name="Corp B").first()
    r = staff_client.get(
        f"/reports/current-employment/export.csv?program_id=&employer_id={emp_b.id}"
    )
    assert r.status_code == 200, r.text[:400]
    reader = csv.reader(io.StringIO(r.text))
    next(reader)
    rows = list(reader)
    assert len(rows) == 1, f"Expected 1 CSV row for Corp B, got {len(rows)}"
