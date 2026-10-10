"""Onyx Reborn — FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.config import get_settings
from app.routers import public as public_router
from app.routers import dashboard as dashboard_router

settings = get_settings()

app = FastAPI(
    title="Onyx Reborn",
    description="BSSI Student Information System — Modernized",
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET,
    session_cookie="onyx_session",
    https_only=False,  # flip to True in cloud deployment
    same_site="lax",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(public_router.router)
app.include_router(dashboard_router.router)
