"""Application settings loaded from environment / .env file."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

# Sentinel value used when a required secret has not been set.
# Code that consumes these keys must call _require() before use.
_UNSET = ""


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DATABASE_URL: str = "sqlite:///./onyx.db"
    # Empty string means "not configured" — the app and reset_db.py will
    # abort with a clear message rather than silently using a random key.
    SESSION_SECRET: str = _UNSET
    ENV: str = "dev"
    DEMO_MODE: bool = True
    PORTAL_ENABLED: bool = True
    MFA_ENC_KEY: str = _UNSET


def _require(value: str, name: str) -> str:
    """Return *value* or raise RuntimeError if it is the empty sentinel."""
    if not value:
        raise RuntimeError(
            f"\n\n  ✗ {name} is not set in your .env file.\n"
            f"  Copy .env.example to .env and fill in all required values.\n"
            f"  Generate MFA_ENC_KEY with:\n"
            f"    python -c \"from cryptography.fernet import Fernet; "
            f"print(Fernet.generate_key().decode())\"\n"
        )
    return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
