import pytest
from app import create_app
from infraestructure.db import db
from domain.user import User
from services.task_service import TaskService
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
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture 
def service(app):
    return TaskService()

def register(client, username, email, password):
    return client.post("/register", data = {
        "username": username,
        "email": email,
        "password": password
    }, follow_redirects = True)

def login(client, email, password):
    return client.post("/login", data = {
        "email": email,
        "password": password
    }, follow_redirects = True)


# ------------------------
# Authentication tests
# ------------------------

def test_user_registration_and_login(client):
    register(client, "testuser", "test@test.com", "password")
    response = login(client, "test@test.com", "password")

    assert response.status_code == 200

def test_board_requires_authentication(client):
    response = client.get("/", follow_redirects = False)

    # Should redirect to login
    assert response.status_code == 302
    assert "/login" in response.location

# ----------------------
# Ownership tests
# ----------------------

def test_users_cannot_see_each_other_tasks(app, service):
    with app.app_context():

        user1 = User(
            username = "user1",
            email = "user1@test.com",
            password_hash = generate_password_hash("pass")
        )

        user2 = User(
            username = "user2",
            email = "user2@test.com",
            password_hash = generate_password_hash("pass")
        )

        db.session.add_all([user1, user2])
        db.session.commit()

        service.create_task("Task 1", "", user1.id)

        tasks_user1 = service.list_tasks(user1.id)
        tasks_user2 = service.list_tasks(user2.id)

        assert len(tasks_user1) == 1
        assert len(tasks_user2) == 0

def test_user_cannot_modify_other_users_task(app, service):
    with app.app_context():

        user1 = User(
            username = "user1",
            email = "user1@test.com",
            password_hash = generate_password_hash("pass")
        )

        user2 = User(
            username = "user2",
            email = "user2@test.com",
            password_hash = generate_password_hash("pass")
        )

        db.session.add_all([user1, user2])
        db.session.commit()

        service.create_task("Task 1", "", user1.id)
        task = service.list_tasks(user1.id)[0]

        with pytest.raises(ValueError):
            service.delete_task(task.id, user2.id)