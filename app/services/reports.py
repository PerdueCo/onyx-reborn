"""Report queries for /reports.

Current employment report (run-sheet step 8):
  Columns: student name, STU number, program, employer, job title,
           hours per week, hourly rate.
  Scope: current jobs only, using is_current_job() from kpis module
         (single source of truth per D-31).
  Filters: optional program_id and/or employer_id.
"""
from __future__ import annotations

import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.models import Employer, Employment, Program, Student
from app.services.kpis import is_current_job


# ---------------------------------------------------------------------------
# Current employment report
# ---------------------------------------------------------------------------

def get_current_employment(
    db: Session,
    *,
    program_id: int | None = None,
    employer_id: int | None = None,
) -> list[dict[str, Any]]:
    """Return rows for the Current Employment report.

    Each row dict:
        student_name  str   – "Last, First"
        stu_number    str   – e.g. "STU-0001"
        program       str   – program name or "—"
        employer      str   – employer name
        job_title     str
        hours         str   – hours per week or "—"
        rate          str   – "$X.XX" or "—"

    Only current jobs (D-31: start_date <= today AND end_date IS NULL OR end_date > today).
    """
    today = datetime.date.today()

    query = (
        db.query(Employment, Student, Employer, Program)
        .join(Student, Student.id == Employment.student_id)
        .join(Employer, Employer.id == Employment.employer_id)
        .outerjoin(Program, Program.id == Student.program_id)
        .filter(Student.status == "active")
    )

    if program_id is not None:
        query = query.filter(Student.program_id == program_id)

    if employer_id is not None:
        query = query.filter(Employment.employer_id == employer_id)

    # Pull all matching rows then filter to current in Python so we use
    # the shared is_current_job() helper without duplicating SQL logic.
    raw = query.order_by(Student.last_name, Student.first_name).all()

    rows: list[dict[str, Any]] = []
    for job, student, employer, program in raw:
        if not is_current_job(job, today):
            continue
        if program:
            prog_label = f"{program.code} \u2014 {program.name}"
        else:
            prog_label = "\u2014"
        rows.append({
            "student_name": f"{student.last_name}, {student.first_name}",
            "stu_number": student.student_number,
            "program": prog_label,
            "employer": employer.name,
            "job_title": job.job_title,
            "hours": str(job.hours_per_week) if job.hours_per_week is not None else "—",
            "rate": f"${float(job.hourly_rate):.2f}" if job.hourly_rate is not None else "—",
        })
    return rows


# ---------------------------------------------------------------------------
# Filter-option helpers
# ---------------------------------------------------------------------------

def get_programs(db: Session) -> list[Program]:
    """Return active programs ordered by code."""
    return db.query(Program).filter(Program.active == True).order_by(Program.code).all()  # noqa: E712


def get_employers(db: Session) -> list[Employer]:
    """Return active employers ordered by name."""
    return db.query(Employer).filter(Employer.active == True).order_by(Employer.name).all()  # noqa: E712
