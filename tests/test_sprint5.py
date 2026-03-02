import pytest
from app import create_app
from domain.user import User
from infraestructure.db import db
from datetime import datetime, timedelta, timezone
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
        db.drop_all()

@pytest.fixture
def service(app):
    return TaskService()

@pytest.fixture
def test_user1(app):
    user = User(
        username = "testuser1",
        email = "test@test.com",
        password_hash = "fakehash"
    )

    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def test_user2(app):
    user = User(
        username = "testuser2",
        email = "test2@test.com",
        password_hash = "fakehash"
    )

    db.session.add(user)
    db.session.commit()
    return user

def test_default_priority(service, test_user1):
    task = service.create_task("Test Task", "", test_user1.id)

    assert task.priority == "medium"
    assert task.manual_priority is False

def test_auto_escalation(service, test_user1):
    task = service.create_task("Old task", "", test_user1.id)

    task.created_at = datetime.utcnow() - timedelta(days = 7)

    service.auto_adjust_priority(task)

    assert task.priority == "high"

def test_manual_priority_override(service, test_user1):
    task = service.create_task("Task", "", test_user1.id)

    # The user changes the priority
    service.update_priority(task.id, "low", test_user1.id)

    # Days passed
    task.created_at = datetime.now(timezone.utc) - timedelta(days = 10)

    service.auto_adjust_priority(task)

    assert task.priority == "low"
    assert task.manual_priority is True

def test_invalid_priority(service, test_user1):
    task = service.create_task("Task", "", test_user1.id)

    with pytest.raises(ValueError):
        service.update_priority(task.id, "invalid", test_user1.id)

def test_priority_wrong_user(service, test_user1, test_user2):
    task = service.create_task("Task", "", test_user1.id)

    with pytest.raises(ValueError):
        service.update_priority(task.id, "high", test_user2.id)