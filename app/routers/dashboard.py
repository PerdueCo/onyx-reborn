"""Dashboard / Overview route."""
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse(
        request,
        "dashboard/index.html",
        {"current_user": None},  # replaced by real auth in Day 3
    )
