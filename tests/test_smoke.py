"""Smoke tests — Day 1 items 1 and 3.

Verifies that:
- GET /  returns HTTP 200 and the "Onyx Reborn" wordmark.
- GET /about returns HTTP 200.
- GET /dashboard returns HTTP 200 with the sidebar layout.
"""


def test_landing_ok(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Onyx Reborn" in response.text


def test_landing_headline(client):
    """Landing page has the correct headline and a link to /login."""
    response = client.get("/")
    assert response.status_code == 200
    # headline text spans a <br> so test each half separately
    assert "A new chapter for" in response.text
    assert "student success" in response.text
    assert 'href="/login"' in response.text


def test_about_ok(client):
    response = client.get("/about")
    assert response.status_code == 200


def test_dashboard_ok(client):
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "Overview" in response.text
    assert "sidebar" in response.text   # layout class present
    assert "DEV MODE" in response.text  # dev banner shown when no user
