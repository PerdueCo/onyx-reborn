"""KPI queries for the dashboard.

spec.md §6 — counts use today's date as the "as_of" date.
Current job = start_date <= today AND (end_date IS NULL OR end_date >= today).
All counts distinguish jobs from distinct students.
"""
from __future__ import annotations

import datetime
from typing import Any

from sqlalchemy import distinct, func
from sqlalchemy.orm import Session

from app.models import AuditEvent, Employment, Student, UserAccount


def _today() -> datetime.date:
    return datetime.date.today()


def get_kpis(db: Session) -> dict[str, Any]:
    """Return dashboard KPI dict.

    Keys
    ----
    total_students      int   – active students
    employed_count      int   – distinct students with ≥1 current job
    employed_pct        int   – round(employed/total * 100) or 0
    current_jobs        int   – total current job rows (may be > employed_count)
    avg_hourly_rate     str   – "$X.XX" or "—" if no rate data
    seeking_count       int   – students where seeking_employment = True
    """
    today = _today()

    total_students: int = (
        db.query(func.count(Student.id))
        .filter(Student.status == "active")
        .scalar()
        or 0
    )

    # Distinct students with at least one current job
    employed_count: int = (
        db.query(func.count(distinct(Employment.student_id)))
        .join(Student, Student.id == Employment.student_id)
        .filter(
            Student.status == "active",
            Employment.start_date <= today,
            (Employment.end_date == None) | (Employment.end_date >= today),  # noqa: E711
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
            (Employment.end_date == None) | (Employment.end_date >= today),  # noqa: E711
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
            (Employment.end_date == None) | (Employment.end_date >= today),  # noqa: E711
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

    return {
        "total_students": total_students,
        "employed_count": employed_count,
        "employed_pct": employed_pct,
        "current_jobs": current_jobs,
        "avg_hourly_rate": avg_hourly_rate,
        "seeking_count": seeking_count,
    }


def get_recent_activity(db: Session, limit: int = 10) -> list[dict[str, Any]]:
    """Return the last *limit* audit events, newest first.

    Each item: {actor_name, event_type, entity_type, entity_id, occurred_at}
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
        events.append(
            {
                "actor_name": actor_name or "System",
                "event_type": ev.event_type,
                "entity_type": ev.entity_type,
                "entity_id": ev.entity_id,
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
        events.append(
            {
                "actor_name": actor_name or "Unknown",
                "event_type": ev.event_type,
                "entity_type": ev.entity_type,
                "entity_id": ev.entity_id,
                "occurred_at": ev.occurred_at,
            }
        )
    return events
