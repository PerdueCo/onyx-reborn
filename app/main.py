"""Onyx Reborn — FastAPI application entry point."""
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.templates_env import templates as _templates

from app.config import _require, get_settings
from app.routers import public as public_router
from app.routers import auth as auth_router
from app.routers import dashboard as dashboard_router
from app.routers import students as students_router
from app.routers import employment as employment_router
from app.routers import reports as reports_router

settings = get_settings()

# ── Startup guard ────────────────────────────────────────────────────────────
# Abort immediately with a clear message if required secrets are missing.
# This prevents the app from booting with a random/empty key and silently
# encrypting TOTP secrets that can never be decrypted after a restart.
_require(settings.SESSION_SECRET, "SESSION_SECRET")
_require(settings.MFA_ENC_KEY, "MFA_ENC_KEY")

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
app.include_router(auth_router.router)
app.include_router(dashboard_router.router)
app.include_router(students_router.router)
app.include_router(employment_router.router)
app.include_router(reports_router.router)

# ---------------------------------------------------------------------------
# Jinja2 globals — registered on the single shared Environment
# ---------------------------------------------------------------------------

# Register csrf_token so every template can call {{ csrf_token(request) }}
from app.security import csrf_token as _csrf_token_fn  # noqa: E402
_templates.env.globals["csrf_token"] = _csrf_token_fn

# ---------------------------------------------------------------------------
# Exception handlers
# ---------------------------------------------------------------------------


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Render a friendly 403 page; pass through everything else."""
    if exc.status_code == 403:
        # Try to get current_user for the sidebar, but don't fail if unavailable
        try:
            from app.db import SessionLocal
            from app.security import get_current_user, get_user_permissions
            db = SessionLocal()
            try:
                user = get_current_user(request, db)
                user_perms = get_user_permissions(user, db) if user else set()
            finally:
                db.close()
        except Exception:
            user = None
            user_perms = set()
        return _templates.TemplateResponse(
            request,
            "403.html",
            {"current_user": user, "user_perms": user_perms},
            status_code=403,
        )
    # For 303 redirects raised as HTTPExceptions (e.g. from require_permission)
    if exc.status_code == 303:
        from fastapi.responses import RedirectResponse
        location = exc.headers.get("Location", "/login") if exc.headers else "/login"
        return RedirectResponse(location, status_code=303)
    raise exc
