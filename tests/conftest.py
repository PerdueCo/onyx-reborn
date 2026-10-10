"""Pytest configuration and shared fixtures."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.db import Base
from app.main import app as fastapi_app
import app.models as _models  # noqa: F401 — registers all ORM classes with Base


@pytest.fixture(scope="session")
def client():
    """Return a FastAPI TestClient for the whole session."""
    with TestClient(fastapi_app) as c:
        yield c


@pytest.fixture()
def db_session():
    """Yield an isolated in-memory SQLite session for schema tests.

    - StaticPool: every connection inside the same test sees the same DB.
    - PRAGMA foreign_keys=ON: mirrors production behaviour (app/db.py).
    - Base.metadata.create_all: builds all tables without Alembic.
    - Rolled back after each test for isolation.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Enable FK enforcement on every connection (mirrors app/db.py)
    @event.listens_for(engine, "connect")
    def _set_fk_pragma(dbapi_conn, _record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        session.rollback()

    Base.metadata.drop_all(engine)
    engine.dispose()
