import pytest
from domain.user import User
from app import create_app
from infraestructure.db import db
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    app = create_app({
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "TESTING": True
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def authenticated_client(app):
    with app.app_context():
        user = User(
            username = "apiuser",
            email = "api@test.com",
            password_hash = generate_password_hash("password")
        )

        db.session.add(user)
        db.session.commit()

    client = app.test_client()

    client.post("/login", data = {
        "identifier": "api@test.com",
        "password": "password"
    }, follow_redirects = True)

    return client

def test_api_create_task(authenticated_client):
    response = authenticated_client.post("/api/tasks", json = {
        "title": "API Task",
        "description": "Created via API"
    })

    assert response.status_code == 201
    data = response.get_json()

    assert data["title"] == "API Task"
    assert data["status"] == "todo"

def test_api_list_tasks(authenticated_client):
    authenticated_client.post("/api/tasks", json = {
        "title": "Task 1"
    })

    response = authenticated_client.get("/api/tasks")


    assert response.status_code == 200
    data = response.get_json()

    assert len(data) == 1
    assert data[0]["title"] == "Task 1"

def test_api_valid_status_transition(authenticated_client):
    create = authenticated_client.post("/api/tasks", json = {
        "title": "Transition Task"
    })

    task_id = create.get_json()["id"]

    response = authenticated_client.put(f"/api/tasks/{task_id}", json = {
        "status": "doing"
    })

    assert response.status_code == 200
    assert response.get_json()["status"] == "doing"

def test_api_invalid_transition(authenticated_client):
    create = authenticated_client.post("/api/tasks", json = {
        "title": "Invalid Transition"
    })

    task_id = create.get_json()["id"]

    response = authenticated_client.put(f"/api/tasks/{task_id}", json = {
        "status": "done"
    })

    assert response.status_code == 400

def test_api_delete_task(authenticated_client):
    create = authenticated_client.post("/api/tasks", json = {
        "title": "Delete Me"
    })

    task_id = create.get_json()["id"]

    response = authenticated_client.delete(f"/api/tasks/{task_id}")

    assert response.status_code == 204
