"""Admin router — /admin (accounts.manage only).

Provides:
  GET  /admin                 Users table + recent audit log (last 50 events)
  POST /admin/unlock/{uid}    Unlock a locked account (CSRF, audit event)

403 for any user without accounts.manage permission.
"""
import datetime

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app import audit
from app.db import get_db
from app.models import AuditEvent, LocalCredential, Role, UserAccount, UserRole
from app.security import check_csrf, get_user_permissions, require_permission
from app.services.kpis import _fmt_activity
from app.templates_env import templates

router = APIRouter(prefix="/admin", tags=["admin"])
_admin_dep = require_permission("accounts.manage")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ctx(current_user: UserAccount, db: Session) -> dict:
    return {
        "current_user": current_user,
        "user_perms": get_user_permissions(current_user, db),
    }


def _get_users(db: Session) -> list[dict]:
    """Return all user accounts with role, credential status, and last sign-in."""
    users = db.query(UserAccount).order_by(UserAccount.display_name).all()

    # Build a role map: user_id -> role name
    rows = (
        db.query(UserRole.user_account_id, Role.name)
        .join(Role, Role.id == UserRole.role_id)
        .all()
    )
    role_map: dict[int, list[str]] = {}
    for uid, rname in rows:
        role_map.setdefault(uid, []).append(rname)

    # Last sign_in_ok event per user
    last_login_rows = (
        db.query(AuditEvent.actor_account_id, AuditEvent.occurred_at)
        .filter(AuditEvent.event_type == "sign_in_ok")
        .order_by(AuditEvent.occurred_at.desc())
        .all()
    )
    last_login: dict[int, datetime.datetime] = {}
    for uid, ts in last_login_rows:
        if uid not in last_login:
            last_login[uid] = ts

    result = []
    for u in users:
        cred = db.get(LocalCredential, u.id)
        mfa_on = bool(cred and cred.mfa_enabled)
        now = datetime.datetime.utcnow()
        locked = bool(
            cred
            and cred.locked_until is not None
            and cred.locked_until > now
        )
        result.append(
            {
                "user": u,
                "roles": ", ".join(role_map.get(u.id, [])) or "—",
                "mfa_on": mfa_on,
                "locked": locked,
                "status": "Locked" if locked else ("Active" if u.active else "Inactive"),
                "last_sign_in": last_login.get(u.id),
            }
        )
    return result


def _get_audit_log(db: Session, limit: int = 50) -> list[dict]:
    """Return the last *limit* audit events as plain-English sentences."""
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
        events.append(
            {
                "sentence": sentence,
                "event_type": ev.event_type,
                "occurred_at": ev.occurred_at,
                "is_security": ev.event_type in (
                    "sign_in_failed", "account_locked", "access_denied", "account_unlock"
                ),
            }
        )
    return events


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.get("", response_class=HTMLResponse)
async def admin_index(
    request: Request,
    current_user: UserAccount = Depends(_admin_dep),
    db: Session = Depends(get_db),
):
    users = _get_users(db)
    audit_log = _get_audit_log(db, limit=50)
    return templates.TemplateResponse(
        request,
        "admin/index.html",
        {
            **_ctx(current_user, db),
            "users": users,
            "audit_log": audit_log,
        },
    )


@router.post("/unlock/{user_id}", response_class=HTMLResponse)
async def unlock_user(
    user_id: int,
    request: Request,
    csrf_token: str = Form(""),
    current_user: UserAccount = Depends(_admin_dep),
    db: Session = Depends(get_db),
):
    check_csrf(request, csrf_token)
    target = db.get(UserAccount, user_id)
    if target is None:
        return HTMLResponse("User not found", status_code=404)
    cred = db.get(LocalCredential, user_id)
    if cred is not None:
        cred.locked_until = None
        cred.failed_logins = 0
        db.commit()
    audit.log_event(
        db,
        current_user.id,
        "account_unlock",
        "user_account",
        user_id,
        {
            "unlocked_user": target.display_name or target.email or str(user_id),
            "unlocked_by": current_user.display_name or current_user.email,
        },
    )
    return RedirectResponse("/admin", status_code=303)
