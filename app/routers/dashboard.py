"""Dashboard / Overview route."""
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import UserAccount
from app.security import get_user_permissions, require_permission

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

_read_dep = require_permission("students.read")


@router.get("/dashboard")
async def dashboard(
    request: Request,
    current_user: UserAccount = Depends(_read_dep),
    db: Session = Depends(get_db),
):
    user_perms = get_user_permissions(current_user, db)
    return templates.TemplateResponse(
        request,
        "dashboard/index.html",
        {
            "current_user": current_user,
            "user_perms": user_perms,
        },
    )
