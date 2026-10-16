"""Security helpers — hashing, TOTP, CSRF, session, permission gate.

spec.md §4 · decisions.md D-17/D-18/D-30
"""
from __future__ import annotations

import secrets
import datetime
from typing import TYPE_CHECKING

import bcrypt
import pyotp
from cryptography.fernet import Fernet, InvalidToken
from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db import get_db

if TYPE_CHECKING:
    from app.models import UserAccount

# ---------------------------------------------------------------------------
# Password hashing
# ---------------------------------------------------------------------------

def hash_password(plain: str) -> str:
    """Return a bcrypt hash of *plain*."""
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    """Return True if *plain* matches *hashed*."""
    return bcrypt.checkpw(plain.encode(), hashed.encode())


# ---------------------------------------------------------------------------
# Fernet encryption for TOTP secrets (spec.md §4 — never logged)
# ---------------------------------------------------------------------------

def _fernet(settings=None) -> Fernet:
    from app.config import get_settings
    s = settings or get_settings()
    if not s.MFA_ENC_KEY:
        raise RuntimeError(
            "MFA_ENC_KEY is not set. Generate one with: "
            "python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\""
        )
    return Fernet(s.MFA_ENC_KEY.encode())


def encrypt_totp_secret(plain: str) -> str:
    return _fernet().encrypt(plain.encode()).decode()


def decrypt_totp_secret(enc: str) -> str:
    try:
        return _fernet().decrypt(enc.encode()).decode()
    except InvalidToken as exc:
        raise ValueError("TOTP secret decryption failed — check MFA_ENC_KEY") from exc


# ---------------------------------------------------------------------------
# TOTP helpers (pyotp)
# ---------------------------------------------------------------------------

def generate_totp_secret() -> str:
    return pyotp.random_base32()


def totp_uri(secret: str, email: str) -> str:
    return pyotp.totp.TOTP(secret).provisioning_uri(name=email, issuer_name="Onyx Reborn")


def verify_totp(secret: str, code: str, valid_window: int = 1) -> bool:
    return pyotp.TOTP(secret).verify(code, valid_window=valid_window)


# ---------------------------------------------------------------------------
# Recovery codes (8 × 10-char alphanumeric)
# ---------------------------------------------------------------------------

_RECOVERY_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # no O/0/1/I


def generate_recovery_codes() -> tuple[list[str], list[str]]:
    """Return (plaintext_codes, bcrypt_hashes) — show plaintext once, store hashes."""
    plain = [
        "".join(secrets.choice(_RECOVERY_ALPHABET) for _ in range(10))
        for _ in range(8)
    ]
    hashed = [bcrypt.hashpw(c.encode(), bcrypt.gensalt()).decode() for c in plain]
    return plain, hashed


def verify_recovery_code(plain: str, hashes: list[str]) -> int | None:
    """Return the index of the matching hash, or None if no match."""
    code = plain.strip().upper()
    for i, h in enumerate(hashes):
        if bcrypt.checkpw(code.encode(), h.encode()):
            return i
    return None


# ---------------------------------------------------------------------------
# CSRF
# ---------------------------------------------------------------------------

def csrf_token(request: Request) -> str:
    """Read (or lazily create) the CSRF token stored in the session."""
    if "csrf" not in request.session:
        request.session["csrf"] = secrets.token_hex(32)
    return request.session["csrf"]


def check_csrf(request: Request, token_from_form: str) -> None:
    expected = request.session.get("csrf", "")
    if not expected or not secrets.compare_digest(expected, token_from_form or ""):
        raise HTTPException(status_code=403, detail="CSRF token mismatch")


# ---------------------------------------------------------------------------
# Session helpers
# ---------------------------------------------------------------------------

_SESSION_TIMEOUT = datetime.timedelta(minutes=30)


def touch_session(request: Request) -> None:
    """Update the last-active timestamp (called by authenticated routes)."""
    request.session["last_active"] = datetime.datetime.utcnow().isoformat()


def _session_expired(request: Request) -> bool:
    ts = request.session.get("last_active")
    if not ts:
        return True
    try:
        last = datetime.datetime.fromisoformat(ts)
        return (datetime.datetime.utcnow() - last) > _SESSION_TIMEOUT
    except ValueError:
        return True


# ---------------------------------------------------------------------------
# Current-user dependency
# ---------------------------------------------------------------------------

def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
) -> "UserAccount | None":
    """Return the signed-in UserAccount (uid + mfa_ok in session), or None."""
    uid = request.session.get("uid")
    mfa_ok = request.session.get("mfa_ok", False)
    if not uid or not mfa_ok:
        return None
    if _session_expired(request):
        request.session.clear()
        return None
    # lazy import to avoid circular
    from app.models import UserAccount
    user = db.get(UserAccount, uid)
    if user is None or not user.active:
        request.session.clear()
        return None
    touch_session(request)
    return user


def get_user_permissions(user: "UserAccount", db: Session) -> set[str]:
    """Return the set of permission codes held by *user* via their roles."""
    from app.models import Permission, Role, RolePermission, UserRole
    rows = (
        db.query(Permission.code)
        .join(RolePermission, RolePermission.permission_id == Permission.id)
        .join(Role, Role.id == RolePermission.role_id)
        .join(UserRole, UserRole.role_id == Role.id)
        .filter(UserRole.user_account_id == user.id)
        .all()
    )
    return {r[0] for r in rows}


# ---------------------------------------------------------------------------
# Permission dependency factory
# ---------------------------------------------------------------------------

class _RequirePermission:
    """FastAPI dependency that enforces a named permission.

    - Not signed in → redirect to /login
    - Signed in but missing permission → HTTP 403
    """

    def __init__(self, code: str) -> None:
        self.code = code

    def __call__(
        self,
        request: Request,
        db: Session = Depends(get_db),
    ) -> "UserAccount":
        user = get_current_user(request, db)
        if user is None:
            from fastapi.responses import RedirectResponse as _RR
            # Raising an HTTPException with a Location header causes FastAPI to
            # return a redirect response.
            raise HTTPException(
                status_code=status.HTTP_303_SEE_OTHER,
                headers={"Location": f"/login?next={request.url.path}"},
                detail="Not authenticated",
            )
        perms = get_user_permissions(user, db)
        if self.code not in perms:
            raise HTTPException(status_code=403, detail="Permission denied")
        return user


def require_permission(code: str) -> _RequirePermission:
    """Return a FastAPI dependency that requires *code*."""
    return _RequirePermission(code)
