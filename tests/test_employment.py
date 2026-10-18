"""tests/test_employment.py — employment acceptance tests.

End-to-end through HTTP (signed-in TestClient with employment.manage permission):
  - add employer → listed
  - employer name required
  - add job → appears on student detail
  - missing job title rejected
  - end job → end date saved, history preserved, other job unaffected
  - end date before start date rejected (acceptance check 4)
  - negative hours rejected (acceptance check 4)
  - already-ended job returns 400
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
    Employer, Employment, LocalCredential, Role, Student,
    UserAccount, UserRole,
)
from app.security import encrypt_totp_secret, hash_password

ADMIN_EMAIL = "eadmin@onyx.test"
ADMIN_PASSWORD = "OnyxAdmin2026!"
ADMIN_TOTP_SECRET = "JBSWY3DPEHPK3PXP"


# ---------------------------------------------------------------------------
# Fixtures (mirrors test_students.py pattern)
# ---------------------------------------------------------------------------


@pytest.fixture()
def emp_db(db_session: Session) -> Session:
    """Seed roles + admin user into the in-memory DB."""
    from scripts.seed_roles import seed as seed_roles
    seed_roles(db_session)

    user = UserAccount(
        provider="local",
        provider_subject=ADMIN_EMAIL,
        display_name="Emp Admin",
        email=ADMIN_EMAIL,
        active=True,
    )
    db_session.add(user)
    db_session.flush()

    cred = LocalCredential(
        user_account_id=user.id,
        password_hash=hash_password(ADMIN_PASSWORD),
        totp_secret_encrypted=encrypt_totp_secret(ADMIN_TOTP_SECRET),
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
def emp_client(emp_db: Session):
    """TestClient backed by seeded in-memory DB, pre-signed-in as admin."""
    from app.db import get_db

    def _override():
        yield emp_db

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
        data={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD, "csrf_token": csrf},
        follow_redirects=False,
    )
    assert r2.status_code == 303
    r3 = client.get("/mfa/verify")
    csrf2 = re.search(r'name="csrf_token"\s+value="([^"]+)"', r3.text).group(1)
    code = pyotp.TOTP(ADMIN_TOTP_SECRET).now()
    r4 = client.post(
        "/mfa/verify",
        data={"code": code, "csrf_token": csrf2},
        follow_redirects=False,
    )
    assert r4.status_code == 303, f"MFA failed: {r4.text[:300]}"


def _csrf(client: TestClient, url: str) -> str:
    r = client.get(url)
    assert r.status_code == 200, f"GET {url} → {r.status_code}: {r.text[:300]}"
    m = re.search(r'name="csrf_token"\s+value="([^"]+)"', r.text)
    assert m, f"No csrf_token on {url}"
    return m.group(1)


def _make_student(db: Session) -> Student:
    """Create a minimal student directly in DB."""
    from app.models import Student
    n = db.query(Student).count() + 1
    s = Student(
        student_number=f"STU-T{n:03d}",
        first_name="Test",
        last_name=f"Student{n}",
        status="active",
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


def _make_employer(db: Session, name: str = "Acme Corp") -> Employer:
    """Create a minimal employer directly in DB."""
    e = Employer(name=name, active=True)
    db.add(e)
    db.commit()
    db.refresh(e)
    return e


# ---------------------------------------------------------------------------
# Employer tests
# ---------------------------------------------------------------------------


def test_employers_list_requires_auth(client):
    """/employment/employers requires sign-in → 303 to /login."""
    r = client.get("/employment/employers", follow_redirects=False)
    assert r.status_code == 303
    assert "/login" in r.headers.get("location", "")


def test_add_employer_success(emp_client: TestClient):
    """POST /employment/employers/new with valid name → 303, employer listed."""
    csrf = _csrf(emp_client, "/employment/employers/new")
    r = emp_client.post(
        "/employment/employers/new",
        data={
            "csrf_token": csrf,
            "name": "City Library",
            "city": "Springfield",
            "state": "IL",
            "phone": "(555) 555-0199",
        },
        follow_redirects=False,
    )
    assert r.status_code == 303, f"Expected 303, got {r.status_code}: {r.text[:400]}"
    assert r.headers.get("location", "").endswith("/employment/employers")

    r2 = emp_client.get("/employment/employers")
    assert r2.status_code == 200
    assert "City Library" in r2.text
    assert "Springfield" in r2.text


def test_add_employer_name_required(emp_client: TestClient):
    """POST /employment/employers/new without name → 422, error shown."""
    csrf = _csrf(emp_client, "/employment/employers/new")
    r = emp_client.post(
        "/employment/employers/new",
        data={"csrf_token": csrf, "name": ""},
        follow_redirects=False,
    )
    assert r.status_code == 422
    assert "name is required" in r.text.lower()


def test_edit_employer_saves(emp_client: TestClient, emp_db: Session):
    """POST /employment/employers/{id}/edit saves new name."""
    employer = _make_employer(emp_db, "Old Name Corp")
    csrf = _csrf(emp_client, f"/employment/employers/{employer.id}/edit")
    r = emp_client.post(
        f"/employment/employers/{employer.id}/edit",
        data={"csrf_token": csrf, "name": "New Name Corp"},
        follow_redirects=False,
    )
    assert r.status_code == 303
    emp_db.refresh(employer)
    assert employer.name == "New Name Corp"


# ---------------------------------------------------------------------------
# Job add tests
# ---------------------------------------------------------------------------


def test_add_job_success(emp_client: TestClient, emp_db: Session):
    """POST /employment/new with valid data → 303 to student detail; job appears."""
    student = _make_student(emp_db)
    employer = _make_employer(emp_db)

    csrf = _csrf(emp_client, f"/employment/new?student_id={student.id}")
    r = emp_client.post(
        "/employment/new",
        data={
            "csrf_token": csrf,
            "student_id": student.id,
            "employer_id": employer.id,
            "job_title": "Library Aide",
            "job_type": "part_time",
            "start_date": "2026-01-15",
            "hours_per_week": "20",
        },
        follow_redirects=False,
    )
    assert r.status_code == 303, f"Expected 303, got {r.status_code}: {r.text[:400]}"
    assert f"/students/{student.id}" in r.headers.get("location", "")

    # Job appears on student detail
    r2 = emp_client.get(f"/students/{student.id}")
    assert r2.status_code == 200
    assert "Library Aide" in r2.text
    assert "Acme Corp" in r2.text


def test_add_job_missing_title_rejected(emp_client: TestClient, emp_db: Session):
    """POST /employment/new without job title → 422, error shown."""
    student = _make_student(emp_db)
    employer = _make_employer(emp_db, "Title Corp")

    csrf = _csrf(emp_client, f"/employment/new?student_id={student.id}")
    r = emp_client.post(
        "/employment/new",
        data={
            "csrf_token": csrf,
            "student_id": student.id,
            "employer_id": employer.id,
            "job_title": "",
            "job_type": "part_time",
            "start_date": "2026-01-15",
        },
    )
    assert r.status_code == 422
    assert "Job title is required" in r.text


def test_add_job_negative_hours_rejected(emp_client: TestClient, emp_db: Session):
    """Negative hours_per_week → 422, error shown (acceptance check 4)."""
    student = _make_student(emp_db)
    employer = _make_employer(emp_db, "Hours Corp")

    csrf = _csrf(emp_client, f"/employment/new?student_id={student.id}")
    r = emp_client.post(
        "/employment/new",
        data={
            "csrf_token": csrf,
            "student_id": student.id,
            "employer_id": employer.id,
            "job_title": "Tester",
            "job_type": "part_time",
            "start_date": "2026-01-15",
            "hours_per_week": "-5",
        },
    )
    assert r.status_code == 422
    assert "negative" in r.text.lower()


def test_add_job_end_before_start_rejected(emp_client: TestClient, emp_db: Session):
    """end_date before start_date → 422, error shown (acceptance check 4)."""
    student = _make_student(emp_db)
    employer = _make_employer(emp_db, "Date Corp")

    csrf = _csrf(emp_client, f"/employment/new?student_id={student.id}")
    r = emp_client.post(
        "/employment/new",
        data={
            "csrf_token": csrf,
            "student_id": student.id,
            "employer_id": employer.id,
            "job_title": "Tester",
            "job_type": "part_time",
            "start_date": "2026-06-01",
            "end_date": "2026-01-01",
        },
    )
    assert r.status_code == 422
    assert "end date" in r.text.lower()


def test_two_simultaneous_jobs(emp_client: TestClient, emp_db: Session):
    """One student holds two simultaneous jobs (acceptance check 2)."""
    student = _make_student(emp_db)
    emp1 = _make_employer(emp_db, "Bookstore")
    emp2 = _make_employer(emp_db, "Library")

    today = datetime.date.today().isoformat()
    for employer, title in [(emp1, "Sales Clerk"), (emp2, "Shelver")]:
        csrf = _csrf(emp_client, f"/employment/new?student_id={student.id}")
        r = emp_client.post(
            "/employment/new",
            data={
                "csrf_token": csrf,
                "student_id": student.id,
                "employer_id": employer.id,
                "job_title": title,
                "job_type": "part_time",
                "start_date": today,
            },
            follow_redirects=False,
        )
        assert r.status_code == 303, f"Add {title} failed: {r.text[:400]}"

    r = emp_client.get(f"/students/{student.id}")
    assert r.status_code == 200
    assert "Sales Clerk" in r.text
    assert "Shelver" in r.text
    assert r.text.count("Current") >= 2


# ---------------------------------------------------------------------------
# End job tests
# ---------------------------------------------------------------------------


def test_end_job_success(emp_client: TestClient, emp_db: Session):
    """POST /employment/{id}/end saves end_date; job still in history (check 3)."""
    student = _make_student(emp_db)
    employer = _make_employer(emp_db, "End Job Corp")

    # Add a job directly in DB
    job = Employment(
        student_id=student.id,
        employer_id=employer.id,
        job_title="Clerk",
        job_type="part_time",
        start_date=datetime.date(2026, 1, 1),
    )
    emp_db.add(job)
    emp_db.commit()
    emp_db.refresh(job)

    csrf = _csrf(emp_client, f"/employment/{job.id}/end")
    r = emp_client.post(
        f"/employment/{job.id}/end",
        data={"csrf_token": csrf, "end_date": "2026-06-30"},
        follow_redirects=False,
    )
    assert r.status_code == 303, f"Expected 303, got {r.status_code}: {r.text[:400]}"
    assert f"/students/{student.id}" in r.headers.get("location", "")

    emp_db.refresh(job)
    assert job.end_date == datetime.date(2026, 6, 30)

    # Job still visible in history on student detail
    r2 = emp_client.get(f"/students/{student.id}")
    assert r2.status_code == 200
    assert "Clerk" in r2.text
    assert "2026-06-30" in r2.text


def test_end_job_end_date_before_start_rejected(emp_client: TestClient, emp_db: Session):
    """end_date before start_date on end-job form → 422 (acceptance check 4)."""
    student = _make_student(emp_db)
    employer = _make_employer(emp_db, "Date Guard Corp")

    job = Employment(
        student_id=student.id,
        employer_id=employer.id,
        job_title="Guard",
        job_type="full_time",
        start_date=datetime.date(2026, 6, 1),
    )
    emp_db.add(job)
    emp_db.commit()
    emp_db.refresh(job)

    csrf = _csrf(emp_client, f"/employment/{job.id}/end")
    r = emp_client.post(
        f"/employment/{job.id}/end",
        data={"csrf_token": csrf, "end_date": "2026-01-01"},
    )
    assert r.status_code == 422
    assert "end date" in r.text.lower()
    emp_db.refresh(job)
    assert job.end_date is None  # unchanged


def test_end_job_already_ended_returns_400(emp_client: TestClient, emp_db: Session):
    """Trying to end an already-ended job returns 400."""
    student = _make_student(emp_db)
    employer = _make_employer(emp_db, "Already Done Corp")

    job = Employment(
        student_id=student.id,
        employer_id=employer.id,
        job_title="Ex-worker",
        job_type="part_time",
        start_date=datetime.date(2025, 1, 1),
        end_date=datetime.date(2025, 12, 31),
    )
    emp_db.add(job)
    emp_db.commit()
    emp_db.refresh(job)

    r = emp_client.get(f"/employment/{job.id}/end")
    assert r.status_code == 400


def test_end_one_job_leaves_other_intact(emp_client: TestClient, emp_db: Session):
    """Ending one job does not affect the student's other current job (check 3)."""
    student = _make_student(emp_db)
    emp1 = _make_employer(emp_db, "First Place")
    emp2 = _make_employer(emp_db, "Second Place")

    job1 = Employment(
        student_id=student.id, employer_id=emp1.id, job_title="Role A",
        job_type="part_time", start_date=datetime.date(2026, 1, 1),
    )
    job2 = Employment(
        student_id=student.id, employer_id=emp2.id, job_title="Role B",
        job_type="part_time", start_date=datetime.date(2026, 1, 1),
    )
    emp_db.add_all([job1, job2])
    emp_db.commit()
    emp_db.refresh(job1)
    emp_db.refresh(job2)

    csrf = _csrf(emp_client, f"/employment/{job1.id}/end")
    emp_client.post(
        f"/employment/{job1.id}/end",
        data={"csrf_token": csrf, "end_date": "2026-06-30"},
        follow_redirects=False,
    )

    emp_db.refresh(job1)
    emp_db.refresh(job2)
    assert job1.end_date == datetime.date(2026, 6, 30)
    assert job2.end_date is None  # untouched
