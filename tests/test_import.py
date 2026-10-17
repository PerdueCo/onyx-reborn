"""tests/test_import.py — acceptance tests for the legacy importer.

Spec §5 acceptance checks:
  - Field widths sum to exactly 357 (Student) and 238 (Employment).
  - 5 students + 5 employers are imported from the test data pack.
  - Running the importer twice adds no new rows.
  - No SSN digits (900-series) appear in the database after import.
"""
from __future__ import annotations

import json

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.services.legacy_import import (
    EMPLOYMENT_FIELDS,
    EMPLOYMENT_RECORD_LEN,
    STUDENT_FIELDS,
    STUDENT_RECORD_LEN,
    run_import,
)


# ---------------------------------------------------------------------------
# Width assertions (module-level constants)
# ---------------------------------------------------------------------------

def test_student_field_widths_sum_to_357():
    """Spec §5: Student field list must total exactly 357 bytes."""
    total = sum(w for _, w in STUDENT_FIELDS)
    assert total == STUDENT_RECORD_LEN, (
        f"Student widths sum to {total}, expected {STUDENT_RECORD_LEN}. "
        f"Fields: {STUDENT_FIELDS}"
    )


def test_employment_field_widths_sum_to_238():
    """Spec §5: Employment field list must total exactly 238 bytes."""
    total = sum(w for _, w in EMPLOYMENT_FIELDS)
    assert total == EMPLOYMENT_RECORD_LEN, (
        f"Employment widths sum to {total}, expected {EMPLOYMENT_RECORD_LEN}. "
        f"Fields: {EMPLOYMENT_FIELDS}"
    )


# ---------------------------------------------------------------------------
# Import tests (use isolated in-memory DB via db_session fixture)
# ---------------------------------------------------------------------------

def _seed_programs_and_roles(db: Session) -> None:
    """Seed the roles/permissions the importer's audit.log_event needs."""
    # The importer does not require roles; audit just needs a working session.
    pass


def test_import_creates_5_students_and_5_employers(db_session: Session):
    """Spec §5: exactly 5 students and 5 employers imported from the test pack."""
    from app.models import Employer, Student

    result = run_import(db_session)

    assert result["students_created"] == 5, (
        f"Expected 5 students created, got {result['students_created']}"
    )
    assert result["employers_created"] == 5, (
        f"Expected 5 employers created, got {result['employers_created']}"
    )
    assert result["students_skipped"] == 0

    db_students = db_session.query(Student).filter_by(legacy_source=True).count()
    db_employers = db_session.query(Employer).filter(
        Employer.legacy_code.isnot(None),
        Employer.legacy_code.notlike("DEMO%"),
    ).count()

    assert db_students == 5, f"Expected 5 legacy students in DB, found {db_students}"
    assert db_employers == 5, f"Expected 5 legacy employers in DB, found {db_employers}"


def test_import_creates_5_jobs(db_session: Session):
    """Each of the 5 students is linked to an employer → 5 employment rows."""
    from app.models import Employment, Student

    run_import(db_session)

    jobs = (
        db_session.query(Employment)
        .join(Student, Employment.student_id == Student.id)
        .filter(Student.legacy_source == True)  # noqa: E712
        .count()
    )
    assert jobs == 5, f"Expected 5 legacy jobs, found {jobs}"


def test_import_is_idempotent(db_session: Session):
    """Spec §5: running the importer twice must add zero new rows."""
    from app.models import Employer, Employment, Student

    run_import(db_session)

    count_students_1 = db_session.query(Student).count()
    count_employers_1 = db_session.query(Employer).count()
    count_jobs_1      = db_session.query(Employment).count()

    result2 = run_import(db_session)

    count_students_2  = db_session.query(Student).count()
    count_employers_2 = db_session.query(Employer).count()
    count_jobs_2      = db_session.query(Employment).count()

    assert count_students_2 == count_students_1, (
        f"Student count grew on re-import: {count_students_1} → {count_students_2}"
    )
    assert count_employers_2 == count_employers_1, (
        f"Employer count grew on re-import: {count_employers_1} → {count_employers_2}"
    )
    assert count_jobs_2 == count_jobs_1, (
        f"Job count grew on re-import: {count_jobs_1} → {count_jobs_2}"
    )
    assert result2["students_created"] == 0
    assert result2["students_skipped"] == 5


def test_no_ssn_in_db(db_session: Session):
    """Spec §5: no 900-series SSN digits appear anywhere in the DB after import.

    The test data uses 900xxxxxx SSNs (non-production values).
    Strategy: dump every text column of every table and check for the 9-digit
    pattern 9000000xx.
    """
    run_import(db_session)

    # Gather all text/json content via raw SQL on each table
    conn = db_session.connection()
    tables_to_check = [
        # (table, columns)
        ("student",     ["first_name", "last_name", "email", "home_phone",
                         "work_phone", "address", "city", "state", "zip",
                         "high_school", "desired_job"]),
        ("employer",    ["name", "address", "city", "state", "zip", "phone",
                         "company_type", "legacy_code"]),
        ("employment",  ["job_title", "supervisor"]),
        ("audit_event", ["detail"]),
    ]

    # The 900-series SSNs in the test pack are 900000001–900000005
    ssn_pattern = "90000000"

    violations: list[str] = []
    for table, cols in tables_to_check:
        for col in cols:
            rows = conn.execute(
                text(f"SELECT {col} FROM {table} WHERE {col} IS NOT NULL")
            ).fetchall()
            for (val,) in rows:
                val_str = str(val) if not isinstance(val, str) else val
                if ssn_pattern in val_str:
                    violations.append(f"{table}.{col}: {val_str[:60]!r}")

    assert not violations, (
        f"SSN pattern '{ssn_pattern}' found in DB after import:\n"
        + "\n".join(violations)
    )


def test_enrolled_date_parsed(db_session: Session):
    """Student #1 enrolled 01/15/98 → enrolled_date == date(1998, 1, 15)."""
    import datetime
    from app.models import Student

    run_import(db_session)

    # First record: Carter Avery
    s = db_session.query(Student).filter_by(last_name="Carter").first()
    assert s is not None, "Student 'Carter' not found after import"
    assert s.enrolled_date == datetime.date(1998, 1, 15), (
        f"Expected enrolled_date 1998-01-15, got {s.enrolled_date}"
    )


def test_seeking_employment_mapped(db_session: Session):
    """YesNo field: 'N' → False, 'Y' → True after import."""
    from app.models import Student

    run_import(db_session)

    carter = db_session.query(Student).filter_by(last_name="Carter").first()
    assert carter is not None
    assert carter.seeking_employment is False  # Record 1: 'N'

    johnson = db_session.query(Student).filter_by(last_name="Johnson").first()
    assert johnson is not None
    assert johnson.seeking_employment is True   # Record 2: 'Y'


def test_job_type_unknown(db_session: Session):
    """All imported jobs must have job_type='unknown' (D-22)."""
    from app.models import Employment, Student

    run_import(db_session)

    jobs = (
        db_session.query(Employment)
        .join(Student, Employment.student_id == Student.id)
        .filter(Student.legacy_source == True)  # noqa: E712
        .all()
    )
    for job in jobs:
        assert job.job_type == "unknown", (
            f"Job {job.id} has job_type={job.job_type!r}, expected 'unknown'"
        )


def test_start_date_equals_enrolled_date(db_session: Session):
    """Employment.start_date == student.enrolled_date for all imported jobs (D-21)."""
    from app.models import Employment, Student

    run_import(db_session)

    pairs = (
        db_session.query(Student, Employment)
        .join(Employment, Employment.student_id == Student.id)
        .filter(Student.legacy_source == True)  # noqa: E712
        .all()
    )
    for student, job in pairs:
        assert job.start_date == student.enrolled_date, (
            f"Student {student.id}: job.start_date={job.start_date} "
            f"!= enrolled_date={student.enrolled_date}"
        )


def test_audit_event_written(db_session: Session):
    """An audit_event row with event_type='legacy_import' is written."""
    from app.models import AuditEvent

    run_import(db_session)

    evt = (
        db_session.query(AuditEvent)
        .filter_by(event_type="legacy_import")
        .first()
    )
    assert evt is not None, "No legacy_import audit event found"
    assert evt.detail is not None
    assert evt.detail.get("students_created") == 5
