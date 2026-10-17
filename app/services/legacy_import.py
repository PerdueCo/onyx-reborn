"""Legacy importer — spec.md §5.

Reads the *reporting copies* Student.txt (357-byte records, no line-breaks) and
Employment.txt (238-byte records) from docs/legacy-reference/legacy-code-copy/Data/.
Those files are read-only; this module never writes to them.

Rules enforced
--------------
- SS_Number is read and immediately discarded — never stored, never logged.
- Birth Month/Day are discarded (D-20).
- YesNo: 'Y'/'1' → True, 'N'/'0' → False (legacy source used both conventions).
- Legacy Date 'MM/DD/YY' → enrolled_date; Date_Graduated 'MM/DD/YYYY' → date.
- Employment.start_date = student.enrolled_date (D-21); job_type = 'unknown' (D-22).
- Amount → Decimal, strip $ and commas.
- Employer matched/upserted by legacy_code.
- Student linked to employer via Company_Code → one Employment row (end_date NULL).
- Idempotent: skip a student if (first, last, home_phone) already exists with legacy_source.
- Returns a summary dict.
"""
from __future__ import annotations

import os
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

# ---------------------------------------------------------------------------
# Record layout definitions  (name, width) — asserted at module load
# ---------------------------------------------------------------------------

STUDENT_FIELDS: list[tuple[str, int]] = [
    ("Program_Code",    7),
    ("Date",            9),   # enrolled_date MM/DD/YY
    ("Program_Name",   31),
    ("SS_Number",      10),   # DISCARD immediately
    ("Last_Name",      16),
    ("First_Name",     16),
    ("Home_Phone",     16),
    ("Work_Phone",     16),
    ("Address",        31),
    ("City",           31),
    ("State",           3),
    ("Zip",            11),
    ("High_School",    31),
    ("Date_Graduated", 11),
    ("Month",           3),   # birth month — DISCARD (D-20)
    ("Day",             3),   # birth day   — DISCARD (D-20)
    ("YesNo",           2),   # seeking_employment
    ("Description",   101),   # desired_job
    ("Company_Code",    9),
]

EMPLOYMENT_FIELDS: list[tuple[str, int]] = [
    ("Company_Code",         9),
    ("Company_Name",        31),
    ("Address",             26),
    ("City",                31),
    ("State",                3),
    ("Zip",                 11),
    ("Job_Title",           31),
    ("Current_Supervisor",  31),
    ("Phone_Number",        16),
    ("Hours_per_Week",       3),
    ("Amount",              16),
    ("Company_Type",        30),
]

STUDENT_RECORD_LEN   = 357
EMPLOYMENT_RECORD_LEN = 238

# Validate at import time so any typo in the table is caught immediately.
assert sum(w for _, w in STUDENT_FIELDS) == STUDENT_RECORD_LEN, (
    f"Student field widths sum to {sum(w for _, w in STUDENT_FIELDS)}, expected {STUDENT_RECORD_LEN}"
)
assert sum(w for _, w in EMPLOYMENT_FIELDS) == EMPLOYMENT_RECORD_LEN, (
    f"Employment field widths sum to {sum(w for _, w in EMPLOYMENT_FIELDS)}, expected {EMPLOYMENT_RECORD_LEN}"
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_DATA_DIR = Path(__file__).parent.parent.parent / "docs" / "legacy-reference" / "legacy-code-copy" / "Data"


def _parse_records(raw: bytes, fields: list[tuple[str, int]], record_len: int) -> list[dict[str, str]]:
    """Decode cp1252, chunk by record_len, strip each field."""
    text = raw.decode("cp1252")
    records = []
    for i in range(0, len(text), record_len):
        chunk = text[i : i + record_len]
        if len(chunk) < record_len:
            break
        rec: dict[str, str] = {}
        offset = 0
        for name, width in fields:
            rec[name] = chunk[offset : offset + width].strip()
            offset += width
        records.append(rec)
    return records


def _parse_date_2y(value: str) -> date | None:
    """MM/DD/YY → date.  Pivot: 00-29 → 2000, 30-99 → 1900."""
    if not value:
        return None
    try:
        m, d, y2 = value.split("/")
        y = int(y2)
        year = 2000 + y if y < 30 else 1900 + y
        return date(year, int(m), int(d))
    except Exception:
        return None


def _parse_date_4y(value: str) -> date | None:
    """MM/DD/YYYY → date."""
    if not value:
        return None
    try:
        m, d, y = value.split("/")
        return date(int(y), int(m), int(d))
    except Exception:
        return None


def _parse_yesno(value: str) -> bool | None:
    v = value.strip().upper()
    if v in ("Y", "1"):
        return True
    if v in ("N", "0"):
        return False
    return None


def _parse_amount(value: str) -> Decimal | None:
    cleaned = value.replace("$", "").replace(",", "").strip()
    if not cleaned:
        return None
    try:
        return Decimal(cleaned)
    except InvalidOperation:
        return None


def _next_student_number(db: Session) -> str:
    from app.models import Student
    last = (
        db.query(Student)
        .filter(Student.student_number.like("STU-%"))
        .order_by(Student.id.desc())
        .first()
    )
    if last:
        try:
            n = int(last.student_number.split("-")[1]) + 1
        except (IndexError, ValueError):
            n = 1
    else:
        n = 1
    return f"STU-{n:04d}"


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def run_import(db: Session) -> dict[str, Any]:
    """Import Student.txt and Employment.txt into the database.

    Returns a summary dict with counts.  Safe to call multiple times.
    """
    from app.models import Employer, Employment, Program, Student
    import app.audit as audit

    student_file    = _DATA_DIR / "Student.txt"
    employment_file = _DATA_DIR / "Employment.txt"

    student_raw    = student_file.read_bytes()
    employment_raw = employment_file.read_bytes()

    student_records    = _parse_records(student_raw,    STUDENT_FIELDS,    STUDENT_RECORD_LEN)
    employment_records = _parse_records(employment_raw, EMPLOYMENT_FIELDS, EMPLOYMENT_RECORD_LEN)

    # Build employer lookup keyed by Company_Code
    employer_by_code: dict[str, Employer] = {}
    emp_created = 0
    for erec in employment_records:
        code = erec["Company_Code"]
        if not code:
            continue
        existing = db.query(Employer).filter_by(legacy_code=code).first()
        if existing:
            employer_by_code[code] = existing
        else:
            employer = Employer(
                name=erec["Company_Name"] or code,
                address=erec["Address"] or None,
                city=erec["City"] or None,
                state=erec["State"] or None,
                zip=erec["Zip"] or None,
                phone=erec["Phone_Number"] or None,
                company_type=erec["Company_Type"] or None,
                legacy_code=code,
                active=True,
            )
            db.add(employer)
            db.flush()
            employer_by_code[code] = employer
            emp_created += 1

    # Build program lookup by code
    program_by_code: dict[str, Program] = {}
    for row in db.query(Program).all():
        program_by_code[row.code] = row

    ssn_count = 0
    students_created = 0
    jobs_created = 0
    students_skipped = 0

    for srec in student_records:
        # Discard SSN — count it but never store it
        _ssn = srec["SS_Number"]  # noqa: F841 — read and discarded
        ssn_count += 1

        first = srec["First_Name"]
        last  = srec["Last_Name"]
        home_phone = srec["Home_Phone"] or None

        # Idempotency: skip if legacy student already exists with same (first, last, home_phone)
        dup_q = (
            db.query(Student)
            .filter(
                Student.first_name == first,
                Student.last_name  == last,
                Student.legacy_source == True,  # noqa: E712
            )
        )
        if home_phone:
            dup_q = dup_q.filter(Student.home_phone == home_phone)
        if dup_q.first():
            students_skipped += 1
            continue

        prog_code = srec["Program_Code"]
        prog_name = srec["Program_Name"]
        program = program_by_code.get(prog_code)
        if not program and prog_code:
            program = Program(code=prog_code, name=prog_name or prog_code, active=True)
            db.add(program)
            db.flush()
            program_by_code[prog_code] = program

        enrolled_date   = _parse_date_2y(srec["Date"])
        date_graduated  = _parse_date_4y(srec["Date_Graduated"])
        # Month and Day (birthday) are deliberately not parsed — D-20
        seeking = _parse_yesno(srec["YesNo"])

        student = Student(
            student_number    = _next_student_number(db),
            first_name        = first,
            last_name         = last,
            home_phone        = home_phone,
            work_phone        = srec["Work_Phone"] or None,
            address           = srec["Address"] or None,
            city              = srec["City"] or None,
            state             = srec["State"] or None,
            zip               = srec["Zip"] or None,
            high_school       = srec["High_School"] or None,
            date_graduated    = date_graduated,
            enrolled_date     = enrolled_date,
            seeking_employment= seeking,
            desired_job       = srec["Description"] or None,
            program_id        = program.id if program else None,
            status            = "active",
            legacy_source     = True,
        )
        db.add(student)
        db.flush()
        students_created += 1

        # Create employment row if a matching employer exists
        company_code = srec["Company_Code"]
        employer = employer_by_code.get(company_code)
        if employer:
            # Find matching employment record for hourly_rate and supervisor
            erec_match = next(
                (e for e in employment_records if e["Company_Code"] == company_code),
                None,
            )
            hourly_rate  = _parse_amount(erec_match["Amount"]) if erec_match else None
            supervisor   = erec_match["Current_Supervisor"] if erec_match else None
            job_title    = erec_match["Job_Title"] if erec_match else "Unknown"
            hours_str    = erec_match["Hours_per_Week"] if erec_match else ""
            try:
                hours = int(hours_str) if hours_str else None
            except ValueError:
                hours = None

            job = Employment(
                student_id    = student.id,
                employer_id   = employer.id,
                job_title     = job_title or "Unknown",
                job_type      = "unknown",
                hours_per_week= hours,
                start_date    = enrolled_date or date(1998, 1, 1),
                end_date      = None,
                supervisor    = supervisor or None,
                hourly_rate   = hourly_rate,
            )
            db.add(job)
            db.flush()
            jobs_created += 1

    db.commit()

    summary = {
        "students_created": students_created,
        "students_skipped": students_skipped,
        "employers_created": emp_created,
        "jobs_created": jobs_created,
        "ssn_count": ssn_count,
    }

    # Audit event (actor_account_id=None — system import)
    audit.log_event(
        db,
        user_id=None,
        action="legacy_import",
        entity_type="student",
        entity_id=None,
        detail=summary,
    )

    return summary
