"""Audit event logger."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def log_event(
    db: "Session",
    user_id: int | None,
    action: str,
    entity: str | None = None,
    detail: str | None = None,
) -> None:
    """Write an audit_event row.

    Placeholder until models.py and the AuditEvent table exist.
    """
    # Full implementation comes in the models/Alembic step.
    pass
