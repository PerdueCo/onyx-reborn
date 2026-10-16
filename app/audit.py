"""Audit event logger.

Writes append-only AuditEvent rows.  Never raises — auth flows must not break
because an audit write failed.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def log_event(
    db: "Session",
    user_id: int | None,
    action: str,
    entity_type: str | None = None,
    entity_id: int | None = None,
    detail: dict[str, Any] | None = None,
) -> None:
    """Insert an AuditEvent row and commit.

    Parameters
    ----------
    db          : active SQLAlchemy session
    user_id     : actor's user_account.id (None for unauthenticated events)
    action      : event_type string e.g. 'sign_in_ok', 'student_create'
    entity_type : table/entity name e.g. 'student', 'user_account'
    entity_id   : PK of the entity (None for session-level events)
    detail      : small allowlisted dict — no passwords, no TOTP secrets
    """
    try:
        from app.models import AuditEvent  # lazy to avoid circular import at module level
        event = AuditEvent(
            actor_account_id=user_id,
            event_type=action,
            entity_type=entity_type or "",
            entity_id=entity_id,
            detail=detail,
        )
        db.add(event)
        db.commit()
    except Exception:
        # best-effort: never let audit failure break a user-facing flow
        try:
            db.rollback()
        except Exception:
            pass
