"""KPI queries for the dashboard.

spec.md §6 / decisions.md D-31
Current job = start_date <= today AND (end_date IS NULL OR end_date > today).
Strict > on end_date: a job whose end_date == today is already history.
All counts distinguish jobs from distinct students.
"""
from __future__ import annotations

import datetime
from typing import Any

from sqlalchemy import distinct, func
from sqlalchemy.orm import Session

from app.models import AuditEvent, Employer, Employment, Program, Student, UserAccount


def _today() -> datetime.date:
    return datetime.date.today()


# ---------------------------------------------------------------------------
# D-31 helper — single source of truth for "is this job current?"
# ---------------------------------------------------------------------------

def is_current_job(job: Employment, today: datetime.date) -> bool:
    """Return True if *job* is currently active as of *today* (D-31).

    current = start_date <= today AND (end_date IS NULL OR end_date > today)
    """
    if job.start_date > today:
        return False
    if job.end_date is None:
        return True
    return job.end_date > today


# ---------------------------------------------------------------------------
# KPIs
# ---------------------------------------------------------------------------

def get_kpis(db: Session) -> dict[str, Any]:
    """Return dashboard KPI dict with a one-sentence briefing.

    Keys
    ----
    total_students      int   – active students
    employed_count      int   – distinct students with ≥1 current job
    employed_pct        int   – round(employed/total * 100) or 0
    current_jobs        int   – total current job rows (may be > employed_count)
    avg_hourly_rate     str   – "$X.XX" or "—" if no rate data
    seeking_count       int   – students where seeking_employment = True
    briefing            str   – one-sentence summary built from real numbers
    """
    today = _today()

    total_students: int = (
        db.query(func.count(Student.id))
        .filter(Student.status == "active")
        .scalar()
        or 0
    )

    # Distinct students with at least one current job (D-31: end_date > today)
    employed_count: int = (
        db.query(func.count(distinct(Employment.student_id)))
        .join(Student, Student.id == Employment.student_id)
        .filter(
            Student.status == "active",
            Employment.start_date <= today,
            (Employment.end_date == None) | (Employment.end_date > today),  # noqa: E711
        )
        .scalar()
        or 0
    )

    employed_pct: int = (
        round(employed_count / total_students * 100) if total_students else 0
    )

    # Total current job rows (can be > employed_count for dual-job students)
    current_jobs: int = (
        db.query(func.count(Employment.id))
        .join(Student, Student.id == Employment.student_id)
        .filter(
            Student.status == "active",
            Employment.start_date <= today,
            (Employment.end_date == None) | (Employment.end_date > today),  # noqa: E711
        )
        .scalar()
        or 0
    )

    # Average hourly rate across current jobs (only rows with a rate)
    avg_raw = (
        db.query(func.avg(Employment.hourly_rate))
        .join(Student, Student.id == Employment.student_id)
        .filter(
            Student.status == "active",
            Employment.start_date <= today,
            (Employment.end_date == None) | (Employment.end_date > today),  # noqa: E711
            Employment.hourly_rate != None,  # noqa: E711
        )
        .scalar()
    )
    avg_hourly_rate: str = f"${float(avg_raw):.2f}" if avg_raw is not None else "—"

    seeking_count: int = (
        db.query(func.count(Student.id))
        .filter(Student.status == "active", Student.seeking_employment == True)  # noqa: E712
        .scalar()
        or 0
    )

    # Top program by employment rate (for briefing sentence)
    top_program_name = _top_program_name(db, today)
    briefing = (
        f"{employed_pct}% of active students are currently employed"
        + (f", led by {top_program_name}" if top_program_name else "")
        + "."
    )

    return {
        "total_students": total_students,
        "employed_count": employed_count,
        "employed_pct": employed_pct,
        "current_jobs": current_jobs,
        "avg_hourly_rate": avg_hourly_rate,
        "seeking_count": seeking_count,
        "briefing": briefing,
    }


def _top_program_name(db: Session, today: datetime.date) -> str:
    """Return the program name with the highest employment rate, or ''."""
    rows = (
        db.query(Program.name, func.count(distinct(Employment.student_id)).label("cnt"))
        .join(Student, Student.program_id == Program.id)
        .join(Employment, Employment.student_id == Student.id)
        .filter(
            Student.status == "active",
            Employment.start_date <= today,
            (Employment.end_date == None) | (Employment.end_date > today),  # noqa: E711
        )
        .group_by(Program.id)
        .order_by(func.count(distinct(Employment.student_id)).desc())
        .first()
    )
    return rows[0] if rows else ""


# ---------------------------------------------------------------------------
# Employment rate by program (bar chart)
# ---------------------------------------------------------------------------

def get_employment_by_program(db: Session) -> list[dict[str, Any]]:
    """Return up to 5 programs sorted by employment rate high→low.

    Each item:
        program_name  str   – short display name
        employed      int   – students with a current job in this program
        total         int   – active students in this program
        pct           int   – round(employed/total*100)

    Programs with 0 active students are excluded.
    """
    today = _today()

    # Total active students per program
    totals = dict(
        db.query(Program.id, func.count(Student.id))
        .join(Student, Student.program_id == Program.id)
        .filter(Student.status == "active")
        .group_by(Program.id)
        .all()
    )

    # Currently employed students per program
    employed = dict(
        db.query(Program.id, func.count(distinct(Employment.student_id)))
        .join(Student, Student.program_id == Program.id)
        .join(Employment, Employment.student_id == Student.id)
        .filter(
            Student.status == "active",
            Employment.start_date <= today,
            (Employment.end_date == None) | (Employment.end_date > today),  # noqa: E711
        )
        .group_by(Program.id)
        .all()
    )

    programs = db.query(Program).filter(Program.active == True).all()  # noqa: E712
    rows = []
    for p in programs:
        total = totals.get(p.id, 0)
        if total == 0:
            continue
        emp_count = employed.get(p.id, 0)
        rows.append(
            {
                "program_name": f"{p.code} \u2014 {p.name}",
                "employed": emp_count,
                "total": total,
                "pct": round(emp_count / total * 100),
            }
        )

    rows.sort(key=lambda r: r["pct"], reverse=True)
    return rows[:5]


# ---------------------------------------------------------------------------
# Top employers (by students currently employed)
# ---------------------------------------------------------------------------

def get_top_employers(db: Session, limit: int = 5) -> list[dict[str, Any]]:
    """Return top *limit* employers by distinct students currently employed.

    Each item:
        name          str  – employer name
        company_type  str  – type or "—"
        student_count int  – distinct students currently employed
        avg_rate      str  – "$X.XX" or "—"
    """
    today = _today()

    rows = (
        db.query(
            Employer.id,
            Employer.name,
            Employer.company_type,
            func.count(distinct(Employment.student_id)).label("cnt"),
            func.avg(Employment.hourly_rate).label("avg_rate"),
        )
        .join(Employment, Employment.employer_id == Employer.id)
        .join(Student, Student.id == Employment.student_id)
        .filter(
            Employer.active == True,  # noqa: E712
            Student.status == "active",
            Employment.start_date <= today,
            (Employment.end_date == None) | (Employment.end_date > today),  # noqa: E711
        )
        .group_by(Employer.id)
        .order_by(func.count(distinct(Employment.student_id)).desc())
        .limit(limit)
        .all()
    )

    result = []
    for _id, name, company_type, cnt, avg_rate in rows:
        result.append(
            {
                "name": name,
                "company_type": company_type or "—",
                "student_count": cnt,
                "avg_rate": f"${float(avg_rate):.2f}" if avg_rate is not None else "—",
            }
        )
    return result


# ---------------------------------------------------------------------------
# Recent activity — plain-English sentences
# ---------------------------------------------------------------------------

_ACTION_LABELS = {
    "student_create": "added",
    "student_edit": "edited",
    "employer_create": "added employer",
    "employer_edit": "edited employer",
    "job_add": "added a job for",
    "job_end": "ended a job for",
    "sign_in_ok": "signed in",
    "sign_in_failed": "failed sign-in attempt",
    "access_denied": "was denied access",
    "account_locked": "Account locked",
    "account_unlock": "unlocked account",
    "import_run": "ran legacy import",
}


def _fmt_activity(event_type: str, actor_name: str, detail: dict | None) -> str:
    """Build a human-readable sentence from an audit event."""
    detail = detail or {}
    actor = actor_name or "System"

    if event_type == "student_create":
        student_name = detail.get("student_name", "")
        stu_num = detail.get("student_number", "")
        if student_name and stu_num:
            return f"{actor} added {student_name}, {stu_num}"
        return f"{actor} added a student"

    if event_type == "student_edit":
        student_name = detail.get("student_name", "")
        stu_num = detail.get("student_number", "")
        if student_name:
            return f"{actor} edited {student_name}{', ' + stu_num if stu_num else ''}"
        return f"{actor} edited a student record"

    if event_type == "employer_create":
        name = detail.get("name", "an employer")
        return f"{actor} added employer {name}"

    if event_type == "employer_edit":
        name = detail.get("name", "an employer")
        return f"{actor} edited {name}"

    if event_type == "job_add":
        student_name = detail.get("student_name", "")
        employer_name = detail.get("employer_name", "")
        if student_name and employer_name:
            return f"{actor} added {employer_name} job for {student_name}"
        return f"{actor} added a job"

    if event_type == "job_end":
        student_name = detail.get("student_name", "")
        employer_name = detail.get("employer_name", "")
        if student_name and employer_name:
            return f"{actor} ended the {employer_name} job for {student_name}"
        return f"{actor} ended a job"

    if event_type == "sign_in_ok":
        return f"{actor} signed in"

    if event_type == "sign_in_failed":
        return f"Failed sign-in attempt for {actor}"

    if event_type == "account_locked":
        return f"Account locked — {actor}"

    if event_type == "access_denied":
        return f"{actor} was denied access"

    if event_type == "import_run":
        n = detail.get("imported", "")
        return f"{actor} ran legacy import{(' — ' + str(n) + ' records') if n else ''}"

    if event_type == "account_unlock":
        unlocked_user = detail.get("unlocked_user", "") if detail else ""
        if unlocked_user:
            return f"{actor} unlocked account for {unlocked_user}"
        return f"{actor} unlocked an account"

    # fallback
    return f"{actor}: {event_type.replace('_', ' ')}"


def get_recent_activity(db: Session, limit: int = 10) -> list[dict[str, Any]]:
    """Return the last *limit* audit events as plain-English items.

    Each item:
        sentence      str               – human-readable description
        is_security   bool              – True for lockout events (red text)
        occurred_at   datetime | None
    """
    rows = (
        db.query(AuditEvent, UserAccount.display_name)
        .outerjoin(UserAccount, UserAccount.id == AuditEvent.actor_account_id)
        .order_by(AuditEvent.occurred_at.desc())
        .limit(limit)
        .all()
    )
    events = []
    for ev, actor_name in rows:
        sentence = _fmt_activity(ev.event_type, actor_name or "System", ev.detail)
        is_security = ev.event_type == "account_locked"
        events.append(
            {
                "sentence": sentence,
                "is_security": is_security,
                "event_type": ev.event_type,
                "occurred_at": ev.occurred_at,
            }
        )
    return events


def get_security_events(db: Session, limit: int = 10) -> list[dict[str, Any]]:
    """Return last *limit* security-relevant audit events (admin only).

    Filtered to sign_in_failed, access_denied, account_locked.
    """
    security_types = {"sign_in_failed", "access_denied", "account_locked"}
    rows = (
        db.query(AuditEvent, UserAccount.display_name)
        .outerjoin(UserAccount, UserAccount.id == AuditEvent.actor_account_id)
        .filter(AuditEvent.event_type.in_(security_types))
        .order_by(AuditEvent.occurred_at.desc())
        .limit(limit)
        .all()
    )
    events = []
    for ev, actor_name in rows:
        sentence = _fmt_activity(ev.event_type, actor_name or "Unknown", ev.detail)
        events.append(
            {
                "sentence": sentence,
                "is_security": True,
                "event_type": ev.event_type,
                "occurred_at": ev.occurred_at,
            }
        )
    return events
