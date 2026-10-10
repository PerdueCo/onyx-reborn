"""Schema acceptance tests — Day 1 item 2.

Covers DATABASE_SCHEMA.md §8 checks:
  Check 1: student_number unique + immutable; required fields enforced.
  Check 2: one student can hold two simultaneous jobs (same or different employer).
  Check 4: negative hours, reversed dates, and FK orphans all rejected.
"""
import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from app.models import Employer, Employment, Student


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_student(n: int, db) -> Student:
    """Create and flush a minimal valid student; return the instance."""
    s = Student(
        student_number=f"STU-{n:04d}",
        first_name="Test",
        last_name=f"Student{n}",
    )
    db.add(s)
    db.flush()
    return s


def _make_employer(name: str, db) -> Employer:
    emp = Employer(name=name)
    db.add(emp)
    db.flush()
    return emp


def _today() -> datetime.date:
    return datetime.date.today()


# ---------------------------------------------------------------------------
# Check 1 — student_number uniqueness; required-field validation
# ---------------------------------------------------------------------------

def test_check1_student_number_unique(db_session):
    """Two students cannot share a student_number."""
    _make_student(1, db_session)
    with pytest.raises(IntegrityError):
        _make_student(1, db_session)  # same number → UNIQUE violation


def test_check1_first_name_required(db_session):
    """A student with first_name=None must be rejected."""
    s = Student(
        student_number="STU-9001",
        first_name=None,  # NOT NULL in schema
        last_name="Smith",
    )
    db_session.add(s)
    with pytest.raises(IntegrityError):
        db_session.flush()


# ---------------------------------------------------------------------------
# Check 2 — two simultaneous jobs, including same employer across periods
# ---------------------------------------------------------------------------

def test_check2_two_simultaneous_jobs(db_session):
    """One student can hold two open jobs at the same time (different employers)."""
    student = _make_student(2, db_session)
    employer_a = _make_employer("Campus Bookstore", db_session)
    employer_b = _make_employer("Community Library", db_session)

    today = _today()

    job1 = Employment(
        student_id=student.id,
        employer_id=employer_a.id,
        job_title="Cashier",
        job_type="part_time",
        start_date=today,
    )
    job2 = Employment(
        student_id=student.id,
        employer_id=employer_b.id,
        job_title="Shelver",
        job_type="part_time",
        start_date=today,
    )
    db_session.add_all([job1, job2])
    db_session.flush()  # must not raise

    db_session.refresh(student)
    jobs = (
        db_session.query(Employment)
        .filter(Employment.student_id == student.id)
        .all()
    )
    assert len(jobs) == 2


def test_check2_same_employer_different_periods(db_session):
    """A student may have two employment rows at the same employer in different periods."""
    student = _make_student(3, db_session)
    employer = _make_employer("Campus Bookstore", db_session)

    today = _today()
    past_start = today - datetime.timedelta(days=365)
    past_end = today - datetime.timedelta(days=180)

    old_job = Employment(
        student_id=student.id,
        employer_id=employer.id,
        job_title="Cashier",
        job_type="part_time",
        start_date=past_start,
        end_date=past_end,
    )
    new_job = Employment(
        student_id=student.id,
        employer_id=employer.id,
        job_title="Supervisor",
        job_type="full_time",
        start_date=today,
    )
    db_session.add_all([old_job, new_job])
    db_session.flush()  # must not raise — (student_id, employer_id) not unique

    count = (
        db_session.query(Employment)
        .filter(
            Employment.student_id == student.id,
            Employment.employer_id == employer.id,
        )
        .count()
    )
    assert count == 2


# ---------------------------------------------------------------------------
# Check 4 — constraint enforcement
# ---------------------------------------------------------------------------

def test_check4_negative_hours_rejected(db_session):
    """hours_per_week < 0 must be rejected by the DB CHECK constraint."""
    student = _make_student(4, db_session)
    employer = _make_employer("Acme Corp", db_session)

    bad = Employment(
        student_id=student.id,
        employer_id=employer.id,
        job_title="Intern",
        job_type="part_time",
        start_date=_today(),
        hours_per_week=-1,
    )
    db_session.add(bad)
    with pytest.raises(IntegrityError):
        db_session.flush()


def test_check4_end_before_start_rejected(db_session):
    """end_date < start_date must be rejected by the DB CHECK constraint."""
    student = _make_student(5, db_session)
    employer = _make_employer("Acme Corp", db_session)

    today = _today()
    bad = Employment(
        student_id=student.id,
        employer_id=employer.id,
        job_title="Intern",
        job_type="part_time",
        start_date=today,
        end_date=today - datetime.timedelta(days=1),
    )
    db_session.add(bad)
    with pytest.raises(IntegrityError):
        db_session.flush()


def test_check4_orphan_employment_rejected(db_session):
    """An Employment row with a non-existent student_id must be rejected (FK ON)."""
    employer = _make_employer("Ghost Corp", db_session)

    orphan = Employment(
        student_id=99999,  # no such student
        employer_id=employer.id,
        job_title="Ghost Worker",
        job_type="part_time",
        start_date=_today(),
    )
    db_session.add(orphan)
    with pytest.raises(IntegrityError):
        db_session.flush()
