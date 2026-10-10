"""Pytest configuration and shared fixtures."""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client():
    """Return a FastAPI TestClient for the whole session."""
    with TestClient(app) as c:
        yield c
