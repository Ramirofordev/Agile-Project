import pytest
from services.task_service import TaskService
from domain.task import Task
from domain.user import User
from infraestructure.db import db
from app import create_app

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

def test_create_task(service):
    user = User(
        username = "test",
        email = "test@test.com",
        password_hash = "fakehash"
    )

    db.session.add(user)
    db.session.commit()

    service.create_task("Test", "Desc", user.id)

    tasks = service.list_tasks(user.id)
    assert len(tasks) == 1
    assert tasks[0].title == "Test"
    assert tasks[0].status == "todo"

def test_edit_task(service):
    user = User(
        username = "test",
        email = "test@test.com",
        password_hash = "fakehash"
    )

    db.session.add(user)
    db.session.commit()

    service.create_task("Old title", "Desc", user.id)
    task = service.list_tasks(user.id)[0]

    service.edit_task(task.id, "New title", user.id, "New Desc")

    updated = service.get_task(task.id)
    assert updated.title == "New title"
    assert updated.description == "New Desc"
