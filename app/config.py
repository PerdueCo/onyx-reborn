"""Application settings loaded from environment / .env file."""
import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DATABASE_URL: str = "sqlite:///./onyx.db"
    SESSION_SECRET: str = "dev-secret-change-me"
    ENV: str = "dev"
    DEMO_MODE: bool = True
    PORTAL_ENABLED: bool = True
    # Fernet key for TOTP secret encryption.
    # Left empty by default so pytest runs without a .env file;
    # a proper key is required in production.
    MFA_ENC_KEY: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
