"""Auth router — login, MFA setup/verify, logout.

spec.md §4 · decisions.md D-17/D-18/D-30
"""
from __future__ import annotations

import base64
import datetime
import io

import pyotp
import qrcode
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import audit
from app.db import get_db
from app.models import LocalCredential, UserAccount, UserRole, Role
from app.security import (
    check_csrf,
    csrf_token,
    decrypt_totp_secret,
    encrypt_totp_secret,
    generate_recovery_codes,
    generate_totp_secret,
    get_current_user,
    hash_password,
    totp_uri,
    verify_password,
    verify_recovery_code,
    verify_totp,
)

router = APIRouter(tags=["auth"])
templates = Jinja2Templates(directory="app/templates")

_LOCKOUT_THRESHOLD = 5
_LOCKOUT_MINUTES = 15


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _lookup_credential(db: Session, email: str) -> tuple[UserAccount | None, LocalCredential | None]:
    """Find (user, credential) by email; return (None, None) if not found."""
    user = db.query(UserAccount).filter(
        UserAccount.email == email.strip().lower(),
        UserAccount.provider == "local",
    ).first()
    if not user:
        return None, None
    cred = db.get(LocalCredential, user.id)
    return user, cred


def _qr_png_b64(uri: str) -> str:
    """Return a base64-encoded PNG of the TOTP provisioning URI."""
    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


def _is_fully_signed_in(request: Request, db: Session) -> bool:
    return get_current_user(request, db) is not None


# ---------------------------------------------------------------------------
# GET /login
# ---------------------------------------------------------------------------

@router.get("/login", response_class=HTMLResponse)
async def login_get(
    request: Request,
    next: str = "/dashboard",
    db: Session = Depends(get_db),
):
    if _is_fully_signed_in(request, db):
        return RedirectResponse("/dashboard", status_code=302)
    from app.config import get_settings
    return templates.TemplateResponse(
        request,
        "auth/login.html",
        {
            "csrf": csrf_token(request),
            "next": next,
            "error": None,
            "demo_mode": get_settings().DEMO_MODE,
        },
    )


# ---------------------------------------------------------------------------
# POST /login
# ---------------------------------------------------------------------------

@router.post("/login", response_class=HTMLResponse)
async def login_post(
    request: Request,
    email: str = Form(""),
    password: str = Form(""),
    csrf_token_field: str = Form("", alias="csrf_token"),
    next: str = Form("/dashboard"),
    db: Session = Depends(get_db),
):
    check_csrf(request, csrf_token_field)
    from app.config import get_settings

    def _fail(msg: str) -> HTMLResponse:
        return templates.TemplateResponse(
            request,
            "auth/login.html",
            {
                "csrf": csrf_token(request),
                "next": next,
                "error": msg,
                "demo_mode": get_settings().DEMO_MODE,
            },
            status_code=200,
        )

    user, cred = _lookup_credential(db, email)

    if not user or not cred:
        audit.log_event(db, None, "sign_in_failed", "user_account", None, {"email": email[:64]})
        return _fail("Email or password is incorrect.")

    # Lockout check
    now = datetime.datetime.utcnow()
    if cred.locked_until and cred.locked_until > now:
        minutes_left = max(1, int((cred.locked_until - now).total_seconds() / 60) + 1)
        return _fail(f"Account locked. Try again in {minutes_left} minute(s).")

    # Password check
    if not verify_password(password, cred.password_hash):
        cred.failed_logins = (cred.failed_logins or 0) + 1
        if cred.failed_logins >= _LOCKOUT_THRESHOLD:
            cred.locked_until = now + datetime.timedelta(minutes=_LOCKOUT_MINUTES)
            db.commit()
            audit.log_event(db, user.id, "sign_in_locked", "user_account", user.id)
            return _fail(f"Account locked after {_LOCKOUT_THRESHOLD} failed attempts. Try again in {_LOCKOUT_MINUTES} minutes.")
        db.commit()
        audit.log_event(db, user.id, "sign_in_failed", "user_account", user.id)
        return _fail("Email or password is incorrect.")

    # Password OK — reset counter, stamp session
    cred.failed_logins = 0
    cred.locked_until = None
    db.commit()
    request.session["uid"] = user.id
    request.session["mfa_ok"] = False
    request.session["last_active"] = now.isoformat()
    audit.log_event(db, user.id, "sign_in_password_ok", "user_account", user.id)

    # MFA branch
    if not cred.mfa_enabled:
        return RedirectResponse("/mfa/setup", status_code=303)
    return RedirectResponse("/mfa/verify", status_code=303)


# ---------------------------------------------------------------------------
# GET /mfa/setup
# ---------------------------------------------------------------------------

@router.get("/mfa/setup", response_class=HTMLResponse)
async def mfa_setup_get(request: Request, db: Session = Depends(get_db)):
    uid = request.session.get("uid")
    if not uid:
        return RedirectResponse("/login", status_code=302)

    user = db.get(UserAccount, uid)
    if not user:
        request.session.clear()
        return RedirectResponse("/login", status_code=302)

    cred = db.get(LocalCredential, uid)
    if cred and cred.mfa_enabled:
        # Already enrolled — skip to verify
        return RedirectResponse("/mfa/verify", status_code=302)

    # Generate a new secret, store it unencrypted in session until confirmed
    secret = generate_totp_secret()
    request.session["totp_pending"] = secret

    uri = totp_uri(secret, user.email or user.display_name or "user")
    qr_b64 = _qr_png_b64(uri)

    return templates.TemplateResponse(
        request,
        "auth/mfa_setup.html",
        {
            "csrf": csrf_token(request),
            "qr_b64": qr_b64,
            "secret": secret,
            "error": None,
        },
    )


# ---------------------------------------------------------------------------
# POST /mfa/setup
# ---------------------------------------------------------------------------

@router.post("/mfa/setup", response_class=HTMLResponse)
async def mfa_setup_post(
    request: Request,
    code: str = Form(""),
    csrf_token_field: str = Form("", alias="csrf_token"),
    db: Session = Depends(get_db),
):
    check_csrf(request, csrf_token_field)

    uid = request.session.get("uid")
    if not uid:
        return RedirectResponse("/login", status_code=302)

    secret = request.session.get("totp_pending", "")
    if not secret:
        return RedirectResponse("/mfa/setup", status_code=302)

    if not verify_totp(secret, code.strip()):
        user = db.get(UserAccount, uid)
        uri = totp_uri(secret, user.email or "user") if user else ""
        qr_b64 = _qr_png_b64(uri) if uri else ""
        return templates.TemplateResponse(
            request,
            "auth/mfa_setup.html",
            {
                "csrf": csrf_token(request),
                "qr_b64": qr_b64,
                "secret": secret,
                "error": "That code didn't work. Try the newest code in your app.",
            },
            status_code=200,
        )

    # Code confirmed — encrypt and persist
    cred = db.get(LocalCredential, uid)
    if not cred:
        return RedirectResponse("/login", status_code=302)

    enc_secret = encrypt_totp_secret(secret)
    plain_codes, hashed_codes = generate_recovery_codes()

    cred.totp_secret_encrypted = enc_secret
    cred.mfa_enabled = True
    cred.recovery_codes_hash = hashed_codes
    db.commit()

    # Clear pending secret from session
    request.session.pop("totp_pending", None)

    audit.log_event(db, uid, "mfa_setup", "user_account", uid)

    # Show recovery codes once
    return templates.TemplateResponse(
        request,
        "auth/mfa_recovery.html",
        {"codes": plain_codes},
    )


# ---------------------------------------------------------------------------
# GET /mfa/verify
# ---------------------------------------------------------------------------

@router.get("/mfa/verify", response_class=HTMLResponse)
async def mfa_verify_get(request: Request, db: Session = Depends(get_db)):
    uid = request.session.get("uid")
    if not uid:
        return RedirectResponse("/login", status_code=302)
    if request.session.get("mfa_ok"):
        return RedirectResponse("/dashboard", status_code=302)
    return templates.TemplateResponse(
        request,
        "auth/mfa_verify.html",
        {
            "csrf": csrf_token(request),
            "error": None,
        },
    )


# ---------------------------------------------------------------------------
# POST /mfa/verify
# ---------------------------------------------------------------------------

@router.post("/mfa/verify", response_class=HTMLResponse)
async def mfa_verify_post(
    request: Request,
    code: str = Form(""),
    csrf_token_field: str = Form("", alias="csrf_token"),
    next: str = Form("/dashboard"),
    db: Session = Depends(get_db),
):
    check_csrf(request, csrf_token_field)

    uid = request.session.get("uid")
    if not uid:
        return RedirectResponse("/login", status_code=302)

    cred = db.get(LocalCredential, uid)
    if not cred or not cred.mfa_enabled or not cred.totp_secret_encrypted:
        return RedirectResponse("/mfa/setup", status_code=302)

    plain_code = code.strip()
    secret = decrypt_totp_secret(cred.totp_secret_encrypted)

    # Try TOTP first
    if verify_totp(secret, plain_code):
        request.session["mfa_ok"] = True
        request.session["last_active"] = datetime.datetime.utcnow().isoformat()
        audit.log_event(db, uid, "mfa_ok", "user_account", uid)
        return RedirectResponse(next if next.startswith("/") else "/dashboard", status_code=303)

    # Try recovery codes
    hashes: list[str] = cred.recovery_codes_hash or []
    idx = verify_recovery_code(plain_code, hashes)
    if idx is not None:
        hashes.pop(idx)
        cred.recovery_codes_hash = list(hashes)  # trigger JSON column update
        db.commit()
        request.session["mfa_ok"] = True
        request.session["last_active"] = datetime.datetime.utcnow().isoformat()
        audit.log_event(db, uid, "mfa_recovery_used", "user_account", uid)
        return RedirectResponse(next if next.startswith("/") else "/dashboard", status_code=303)

    audit.log_event(db, uid, "mfa_failed", "user_account", uid)
    return templates.TemplateResponse(
        request,
        "auth/mfa_verify.html",
        {
            "csrf": csrf_token(request),
            "error": "That code didn't work. Try the newest code in your app.",
        },
        status_code=200,
    )


# ---------------------------------------------------------------------------
# POST /logout
# ---------------------------------------------------------------------------

@router.post("/logout", response_class=HTMLResponse)
async def logout(
    request: Request,
    csrf_token_field: str = Form("", alias="csrf_token"),
    db: Session = Depends(get_db),
):
    check_csrf(request, csrf_token_field)
    uid = request.session.get("uid")
    request.session.clear()
    audit.log_event(db, uid, "sign_out", "user_account", uid)
    response = RedirectResponse("/?signed_out=1", status_code=303)
    return response
