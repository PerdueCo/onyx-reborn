"""SQLAlchemy ORM models — all tables for Onyx Reborn.

Source of truth: docs/design/DATABASE_SCHEMA.md §5
Legacy-field additions: docs/plan/spec.md §3
Decisions: decisions.md D-17 through D-25
"""
from __future__ import annotations

import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)

from app.db import Base


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now() -> datetime.datetime:
    return datetime.datetime.utcnow()


# ---------------------------------------------------------------------------
# Identity & access
# ---------------------------------------------------------------------------

class UserAccount(Base):
    """An application account.  One account can optionally link to one Student."""

    __tablename__ = "user_account"
    __table_args__ = (
        UniqueConstraint("provider", "provider_subject", name="uq_provider_subject"),
    )

    id = Column(Integer, primary_key=True)
    provider = Column(String(64), nullable=False)          # e.g. 'local'
    provider_subject = Column(String(256), nullable=False)  # stable subject ID
    display_name = Column(String(128))
    email = Column(String(256))
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=_now)
    updated_at = Column(DateTime, nullable=False, default=_now, onupdate=_now)


class LocalCredential(Base):
    """Local-provider password + TOTP secret.  PK == FK to user_account (D-17)."""

    __tablename__ = "local_credential"

    user_account_id = Column(
        Integer,
        ForeignKey("user_account.id", ondelete="CASCADE"),
        primary_key=True,
    )
    password_hash = Column(String(256), nullable=False)
    totp_secret_encrypted = Column(String(512))          # NULL until MFA enrolled
    mfa_enabled = Column(Boolean, nullable=False, default=False)
    recovery_codes_hash = Column(JSON)                   # list of bcrypt hashes
    failed_logins = Column(Integer, nullable=False, default=0)
    locked_until = Column(DateTime)
    updated_at = Column(DateTime, nullable=False, default=_now, onupdate=_now)


class Role(Base):
    """Named role (Administrator, Staff, Reviewer, Student — D-23)."""

    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)


class UserRole(Base):
    """Many-to-many join between UserAccount and Role.  Composite PK prevents dupes."""

    __tablename__ = "user_role"

    user_account_id = Column(
        Integer,
        ForeignKey("user_account.id", ondelete="CASCADE"),
        primary_key=True,
    )
    role_id = Column(
        Integer,
        ForeignKey("role.id", ondelete="CASCADE"),
        primary_key=True,
    )


class Permission(Base):
    """Named permission code (e.g. 'students.manage' — D-23)."""

    __tablename__ = "permission"

    id = Column(Integer, primary_key=True)
    code = Column(String(64), nullable=False, unique=True)
    description = Column(String(256))


class RolePermission(Base):
    """Many-to-many join between Role and Permission.  Composite PK prevents dupes."""

    __tablename__ = "role_permission"

    role_id = Column(
        Integer,
        ForeignKey("role.id", ondelete="CASCADE"),
        primary_key=True,
    )
    permission_id = Column(
        Integer,
        ForeignKey("permission.id", ondelete="CASCADE"),
        primary_key=True,
    )


# ---------------------------------------------------------------------------
# Program catalog
# ---------------------------------------------------------------------------

class Program(Base):
    """Optional enrollment program.  Provisional; one-program-per-student for now."""

    __tablename__ = "program"

    id = Column(Integer, primary_key=True)
    code = Column(String(32), nullable=False, unique=True)
    name = Column(String(128), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=_now)
    updated_at = Column(DateTime, nullable=False, default=_now, onupdate=_now)


# ---------------------------------------------------------------------------
# Students
# ---------------------------------------------------------------------------

class Student(Base):
    """Core student record.

    student_number: generated STU-#### on creation; immutable via app logic (D-19).
    Legacy optional fields from spec §3 / D-20 (no birth data).
    """

    __tablename__ = "student"
    __table_args__ = (
        CheckConstraint(
            "status IN ('active', 'inactive', 'archived')",
            name="ck_student_status",
        ),
    )

    id = Column(Integer, primary_key=True)
    student_number = Column(String(16), nullable=False, unique=True)

    # Optional link to a login account
    user_account_id = Column(
        Integer,
        ForeignKey("user_account.id", ondelete="SET NULL"),
        unique=True,
    )

    # Required name fields
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)

    # Contact (optional)
    email = Column(String(256))
    home_phone = Column(String(32))   # spec §3: two phones (D-20)
    work_phone = Column(String(32))

    # Program (nullable FK — enrollment model still provisional)
    program_id = Column(Integer, ForeignKey("program.id", ondelete="SET NULL"))

    status = Column(String(16), nullable=False, default="active")

    # Optimistic-locking version (DATABASE_SCHEMA.md §4)
    version = Column(Integer, nullable=False, default=1)

    created_at = Column(DateTime, nullable=False, default=_now)
    updated_at = Column(DateTime, nullable=False, default=_now, onupdate=_now)

    # ------------------------------------------------------------------
    # Legacy optional fields (spec §3 / D-20 — no birth data at all)
    # ------------------------------------------------------------------
    address = Column(String(256))
    city = Column(String(64))
    state = Column(String(32))
    zip = Column(String(16))
    high_school = Column(String(128))
    date_graduated = Column(Date)
    seeking_employment = Column(Boolean)
    desired_job = Column(Text)
    enrolled_date = Column(Date)     # legacy Date field (D-05)
    legacy_source = Column(Boolean, nullable=False, default=False)


# ---------------------------------------------------------------------------
# Employers
# ---------------------------------------------------------------------------

class Employer(Base):
    """Employer / work-site record.

    Names need not be globally unique (DATABASE_SCHEMA.md §5).
    Legacy additions: address, state (bug fix D-06), legacy_code (D-03).
    """

    __tablename__ = "employer"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    active = Column(Boolean, nullable=False, default=True)

    # Legacy optional fields (spec §3)
    address = Column(String(256))
    city = Column(String(64))
    state = Column(String(32))    # D-06: previously never saved
    zip = Column(String(16))
    phone = Column(String(32))
    company_type = Column(String(64))
    legacy_code = Column(String(16))  # old 8-char Company_Code (D-03)

    created_at = Column(DateTime, nullable=False, default=_now)
    updated_at = Column(DateTime, nullable=False, default=_now, onupdate=_now)


# ---------------------------------------------------------------------------
# Employment
# ---------------------------------------------------------------------------

class Employment(Base):
    """One employment period for one student at one employer.

    Multiple simultaneous jobs allowed (DATABASE_SCHEMA.md §5 — no unique on student_id).
    job_type includes 'unknown' for imported rows (D-22).
    hours_per_week CHECK >= 0 (check 4).
    end_date CHECK >= start_date when both present (check 4).
    """

    __tablename__ = "employment"
    __table_args__ = (
        CheckConstraint(
            "job_type IN ('part_time', 'full_time', 'other', 'unknown')",
            name="ck_employment_job_type",
        ),
        CheckConstraint(
            "hours_per_week IS NULL OR hours_per_week >= 0",
            name="ck_employment_hours_non_negative",
        ),
        CheckConstraint(
            "end_date IS NULL OR end_date >= start_date",
            name="ck_employment_end_after_start",
        ),
    )

    id = Column(Integer, primary_key=True)
    student_id = Column(
        Integer,
        ForeignKey("student.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    employer_id = Column(
        Integer,
        ForeignKey("employer.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    job_title = Column(String(128), nullable=False)
    job_type = Column(String(16), nullable=False, default="unknown")
    hours_per_week = Column(Integer)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)

    # Optimistic-locking version (DATABASE_SCHEMA.md §4)
    version = Column(Integer, nullable=False, default=1)

    created_at = Column(DateTime, nullable=False, default=_now)
    updated_at = Column(DateTime, nullable=False, default=_now, onupdate=_now)

    # Legacy optional fields (spec §3)
    supervisor = Column(String(128))
    hourly_rate = Column(Numeric(8, 2))


# ---------------------------------------------------------------------------
# Change requests (optional portal — DATABASE_SCHEMA.md §5 CHANGE_REQUEST)
# ---------------------------------------------------------------------------

class ChangeRequest(Base):
    """Proposed student/employment change submitted through the self-service portal.

    PORTAL_ENABLED gates the routes that create these; the table always exists
    so staff flows work with the portal disabled (D-24 / check 9).
    """

    __tablename__ = "change_request"
    __table_args__ = (
        CheckConstraint(
            "request_type IN ('add_job', 'update_job', 'end_job', 'update_student')",
            name="ck_cr_request_type",
        ),
        CheckConstraint(
            "status IN ('pending', 'needs_correction', 'approved', 'rejected', 'cancelled')",
            name="ck_cr_status",
        ),
    )

    id = Column(Integer, primary_key=True)
    student_id = Column(
        Integer,
        ForeignKey("student.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    submitted_by_account_id = Column(
        Integer,
        ForeignKey("user_account.id", ondelete="RESTRICT"),
        nullable=False,
    )
    request_type = Column(String(32), nullable=False)
    target_employment_id = Column(
        Integer,
        ForeignKey("employment.id", ondelete="SET NULL"),
    )
    applied_employment_id = Column(
        Integer,
        ForeignKey("employment.id", ondelete="SET NULL"),
    )
    proposed_values = Column(JSON)          # allowlisted fields only
    base_record_version = Column(Integer)   # NULL for add_job
    status = Column(String(24), nullable=False, default="pending")
    reviewed_by_account_id = Column(
        Integer,
        ForeignKey("user_account.id", ondelete="SET NULL"),
    )
    review_feedback = Column(Text)
    submitted_at = Column(DateTime, nullable=False, default=_now)
    reviewed_at = Column(DateTime)

    # Optimistic-locking version
    version = Column(Integer, nullable=False, default=1)

    created_at = Column(DateTime, nullable=False, default=_now)
    updated_at = Column(DateTime, nullable=False, default=_now, onupdate=_now)


# ---------------------------------------------------------------------------
# Audit log (append-only — DATABASE_SCHEMA.md §5 AUDIT_EVENT)
# ---------------------------------------------------------------------------

class AuditEvent(Base):
    """Immutable audit record.

    actor_account_id is a loose (non-FK) reference so deleted accounts don't
    destroy history (DATABASE_SCHEMA.md §5 AUDIT_EVENT).
    """

    __tablename__ = "audit_event"

    id = Column(Integer, primary_key=True)
    actor_account_id = Column(Integer)        # NOT a FK — see docstring
    event_type = Column(String(64), nullable=False)
    entity_type = Column(String(64), nullable=False)
    entity_id = Column(Integer)
    change_request_id = Column(Integer)       # loose reference
    occurred_at = Column(DateTime, nullable=False, default=_now)
    detail = Column(JSON)                     # allowlisted minimal summary
