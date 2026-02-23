import pytest
from services.task_service import TaskService
from domain.task import Task
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
    service.create_task("Test task", "Description")

    tasks = service.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Test task"
    assert tasks[0].status == "todo"

def test_edit_task(service):
    service.create_task("Old title", "Desc")
    task = service.list_tasks()[0]

    service.edit_task(task.id, "New title", "New Desc")

    updated = service.get_task(task.id)
    assert updated.title == "New title"
    assert updated.description == "New Desc"
