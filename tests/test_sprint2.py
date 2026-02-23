import pytest
from services.task_service import TaskService
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

def test_delete_task(service):
    service.create_task("Task to delete", "")
    task = service.list_tasks()[0]

    service.delete_task(task.id)

    tasks = service.list_tasks()
    assert len(tasks) == 0

def test_valid_status_transition(service):
    service.create_task("Task", "")
    task = service.list_tasks()[0]

    # todo -> doing
    service.change_status(task.id, "doing")
    updated = service.get_task(task.id) 
    assert updated.status == "doing"

    # doing -> done
    service.change_status(task.id, "done")
    updated = service.get_task(task.id)
    assert updated.status == "done"

def test_invalid_transition(service):
    service.create_task("Task", "")
    task = service.list_tasks()[0]

    # It doesn't allowed todo -> done directly
    with pytest.raises(ValueError):
        service.change_status(task.id, "done")

