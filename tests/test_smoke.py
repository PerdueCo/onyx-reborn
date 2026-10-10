"""Smoke test — Day 1 item 1.

Verifies that:
- GET /  returns HTTP 200 and the "Onyx Reborn" wordmark.
- GET /about returns HTTP 200.
"""


def test_landing_ok(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Onyx Reborn" in response.text


def test_about_ok(client):
    response = client.get("/about")
    assert response.status_code == 200
