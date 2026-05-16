from datetime import datetime, timedelta, UTC

import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from domain.task import Task
from domain.user import User
from infraestructure.db import db
from services.task_service import TaskService


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


def create_user(username="hardening", email="hardening@test.com"):
    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash("password")
    )
    db.session.add(user)
    db.session.commit()
    return user


def login(client, email="hardening@test.com"):
    return client.post("/login", data={
        "identifier": email,
        "password": "password"
    }, follow_redirects=True)


def test_secret_key_is_required_outside_testing_without_env(monkeypatch):
    monkeypatch.delenv("SECRET_KEY", raising=False)

    with pytest.raises(RuntimeError):
        create_app({
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
        })


def test_dev_secret_key_is_allowed_in_testing():
    app = create_app({
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "TESTING": True
    })

    assert app.config["SECRET_KEY"] == "dev_key"


def test_secret_key_from_env_is_used_outside_testing(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "safe-test-secret")

    app = create_app({
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    assert app.config["SECRET_KEY"] == "safe-test-secret"


def test_api_list_tasks_does_not_auto_adjust_priority(app):
    with app.app_context():
        user = create_user()
        old_task = Task(
            title="Old task",
            description="",
            user_id=user.id,
            priority="low",
            created_at=datetime.now(UTC) - timedelta(days=7)
        )
        db.session.add(old_task)
        db.session.commit()
        task_id = old_task.id
        user_email = user.email

    client = app.test_client()
    login(client, user_email)

    response = client.get("/api/tasks")

    assert response.status_code == 200

    with app.app_context():
        task = db.session.get(Task, task_id)
        assert task.priority == "low"


def test_refresh_auto_priorities_adjusts_and_commits(app):
    with app.app_context():
        user = create_user()
        task = Task(
            title="Old task",
            description="",
            user_id=user.id,
            priority="low",
            created_at=datetime.now(UTC) - timedelta(days=7)
        )
        db.session.add(task)
        db.session.commit()
        task_id = task.id

        service = TaskService()
        service.refresh_auto_priorities(user.id)
        db.session.expire_all()

        refreshed = db.session.get(Task, task_id)
        assert refreshed.priority == "high"
