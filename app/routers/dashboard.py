"""Dashboard / Overview route."""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import UserAccount
from app.security import get_user_permissions, require_permission
from app.services.kpis import get_kpis, get_recent_activity, get_security_events
from app.templates_env import templates

router = APIRouter()
_read_dep = require_permission("students.read")


@router.get("/dashboard")
async def dashboard(
    request: Request,
    current_user: UserAccount = Depends(_read_dep),
    db: Session = Depends(get_db),
):
    user_perms = get_user_permissions(current_user, db)
    is_admin = "accounts.manage" in user_perms

    kpis = get_kpis(db)
    recent_activity = get_recent_activity(db, limit=10)
    security_events = get_security_events(db, limit=10) if is_admin else []

    return templates.TemplateResponse(
        request,
        "dashboard/index.html",
        {
            "current_user": current_user,
            "user_perms": user_perms,
            "is_admin": is_admin,
            "kpis": kpis,
            "recent_activity": recent_activity,
            "security_events": security_events,
        },
    )
