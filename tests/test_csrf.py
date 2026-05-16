import re

import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from domain.user import User
from infraestructure.db import db


@pytest.fixture
def app():
    app = create_app({
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "TESTING": True,
        "CSRF_ENABLED": True
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


def create_user():
    user = User(
        username="csrfuser",
        email="csrf@test.com",
        password_hash=generate_password_hash("password")
    )
    db.session.add(user)
    db.session.commit()
    return user


def extract_csrf_token(html):
    match = re.search(r'name\s*=\s*["\']csrf_token["\']\s+value\s*=\s*["\']([^"\']+)', html)
    assert match is not None
    return match.group(1)


def login_with_csrf(client):
    login_page = client.get("/login")
    token = extract_csrf_token(login_page.get_data(as_text=True))

    response = client.post("/login", data={
        "identifier": "csrf@test.com",
        "password": "password",
        "csrf_token": token
    })

    assert response.status_code == 302

    dashboard = client.get("/")
    return extract_csrf_token(dashboard.get_data(as_text=True))


def test_login_post_without_csrf_token_is_rejected(app):
    with app.app_context():
        create_user()

    client = app.test_client()

    response = client.post("/login", data={
        "identifier": "csrf@test.com",
        "password": "password"
    })

    assert response.status_code == 400


def test_login_post_with_csrf_token_is_allowed(app):
    with app.app_context():
        create_user()

    client = app.test_client()

    login_page = client.get("/login")
    token = extract_csrf_token(login_page.get_data(as_text=True))

    response = client.post("/login", data={
        "identifier": "csrf@test.com",
        "password": "password",
        "csrf_token": token
    })

    assert response.status_code == 302
    assert response.headers["Location"] == "/"


def test_csrf_token_regenerates_after_login(app):
    with app.app_context():
        create_user()

    client = app.test_client()
    login_page = client.get("/login")
    anonymous_token = extract_csrf_token(login_page.get_data(as_text=True))

    client.post("/login", data={
        "identifier": "csrf@test.com",
        "password": "password",
        "csrf_token": anonymous_token
    })

    dashboard = client.get("/")
    authenticated_token = extract_csrf_token(dashboard.get_data(as_text=True))

    assert authenticated_token != anonymous_token


def test_csrf_token_regenerates_after_logout(app):
    with app.app_context():
        create_user()

    client = app.test_client()
    token = login_with_csrf(client)

    response = client.post("/logout", data={
        "csrf_token": token
    })
    assert response.status_code == 302

    login_page = client.get("/login")
    logged_out_token = extract_csrf_token(login_page.get_data(as_text=True))

    assert logged_out_token != token


def test_logout_get_is_not_allowed(app):
    with app.app_context():
        create_user()

    client = app.test_client()
    login_with_csrf(client)

    response = client.get("/logout")

    assert response.status_code == 405


def test_logout_post_without_csrf_token_is_rejected(app):
    with app.app_context():
        create_user()

    client = app.test_client()
    login_with_csrf(client)

    response = client.post("/logout")

    assert response.status_code == 400


def test_api_post_requires_csrf_header_when_enabled(app):
    with app.app_context():
        create_user()

    client = app.test_client()
    token = login_with_csrf(client)

    missing_token = client.post("/api/tasks", json={
        "title": "Blocked"
    })

    assert missing_token.status_code == 400

    valid_token = client.post("/api/tasks", json={
        "title": "Allowed"
    }, headers={
        "X-CSRF-Token": token
    })

    assert valid_token.status_code == 201
    assert valid_token.get_json()["title"] == "Allowed"


def test_api_put_requires_csrf_header_when_enabled(app):
    with app.app_context():
        create_user()

    client = app.test_client()
    token = login_with_csrf(client)

    create = client.post("/api/tasks", json={
        "title": "Original"
    }, headers={
        "X-CSRF-Token": token
    })
    task_id = create.get_json()["id"]

    missing_token = client.put(f"/api/tasks/{task_id}", json={
        "title": "Blocked"
    })

    assert missing_token.status_code == 400

    valid_token = client.put(f"/api/tasks/{task_id}", json={
        "title": "Allowed"
    }, headers={
        "X-CSRF-Token": token
    })

    assert valid_token.status_code == 200
    assert valid_token.get_json()["title"] == "Allowed"


def test_api_delete_requires_csrf_header_when_enabled(app):
    with app.app_context():
        create_user()

    client = app.test_client()
    token = login_with_csrf(client)

    create = client.post("/api/tasks", json={
        "title": "Delete Me"
    }, headers={
        "X-CSRF-Token": token
    })
    task_id = create.get_json()["id"]

    missing_token = client.delete(f"/api/tasks/{task_id}")

    assert missing_token.status_code == 400

    valid_token = client.delete(f"/api/tasks/{task_id}", headers={
        "X-CSRF-Token": token
    })

    assert valid_token.status_code == 204


def test_dashboard_renders_csrf_token_for_forms_and_javascript(app):
    with app.app_context():
        create_user()

    client = app.test_client()
    login_with_csrf(client)

    response = client.get("/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'meta name = "csrf-token"' in html
    assert 'name = "csrf_token"' in html
    assert 'action = "/logout" method = "POST"' in html
