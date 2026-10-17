"""Public routes: landing page and About page."""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.templates_env import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    return templates.TemplateResponse(request, "public/landing.html")


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(request, "public/about.html")
