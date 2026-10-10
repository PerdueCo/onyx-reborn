"""Seed roles and permissions defined in decisions.md D-23.

Idempotent: safe to run multiple times.  Uses INSERT-or-ignore semantics via
merge() so re-runs add nothing and raise no errors.

Usage:
    .venv\\Scripts\\python.exe scripts/seed_roles.py
"""
import sys
import os

# Allow running from repo root without installing the package.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy.orm import Session

from app.db import engine
from app.models import Permission, Role, RolePermission  # noqa: F401
import app.models  # noqa: F401 — ensures all tables are registered


# ---------------------------------------------------------------------------
# Data from D-23
# ---------------------------------------------------------------------------

ROLES = ["Administrator", "Staff", "Reviewer", "Student"]

PERMISSIONS = [
    ("students.read",           "View student records"),
    ("students.manage",         "Create and edit student records"),
    ("employment.manage",       "Record and end employment"),
    ("reports.read",            "Run and export reports"),
    ("accounts.manage",         "Create, disable, and reset accounts"),
    ("student_updates.approve", "Approve or reject change requests"),
    ("self_service.use",        "Student self-service portal access"),
]

# Role → list of permission codes
ROLE_PERMISSIONS: dict[str, list[str]] = {
    "Administrator": [
        "students.read",
        "students.manage",
        "employment.manage",
        "reports.read",
        "accounts.manage",
        "student_updates.approve",
        "self_service.use",
    ],
    "Staff": [
        "students.read",
        "students.manage",
        "employment.manage",
        "reports.read",
    ],
    "Reviewer": [
        "student_updates.approve",
    ],
    "Student": [
        "self_service.use",
    ],
}


# ---------------------------------------------------------------------------
# Seeder
# ---------------------------------------------------------------------------

def seed(session: Session) -> None:
    """Insert roles and permissions; skip rows that already exist."""

    # 1. Upsert roles
    role_map: dict[str, Role] = {}
    for name in ROLES:
        existing = session.query(Role).filter_by(name=name).first()
        if existing:
            role_map[name] = existing
        else:
            r = Role(name=name)
            session.add(r)
            session.flush()
            role_map[name] = r

    # 2. Upsert permissions
    perm_map: dict[str, Permission] = {}
    for code, description in PERMISSIONS:
        existing = session.query(Permission).filter_by(code=code).first()
        if existing:
            perm_map[code] = existing
        else:
            p = Permission(code=code, description=description)
            session.add(p)
            session.flush()
            perm_map[code] = p

    # 3. Upsert role→permission assignments
    for role_name, perm_codes in ROLE_PERMISSIONS.items():
        role = role_map[role_name]
        for code in perm_codes:
            perm = perm_map[code]
            existing = (
                session.query(RolePermission)
                .filter_by(role_id=role.id, permission_id=perm.id)
                .first()
            )
            if not existing:
                session.add(RolePermission(role_id=role.id, permission_id=perm.id))

    session.commit()
    print(
        f"Seeded {len(ROLES)} roles, {len(PERMISSIONS)} permissions, "
        f"{sum(len(v) for v in ROLE_PERMISSIONS.values())} role-permission assignments."
    )


if __name__ == "__main__":
    with Session(engine) as s:
        seed(s)
