import pytest
from services.task_service import TaskService
from infraestructure.db import db
from domain.user import User
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

@pytest.fixture
def test_user(app):
    user = User(
        username = "testuser",
        email = "test@test.com",
        password_hash = "fakehash"
    )

    db.session.add(user)
    db.session.commit()
    return user

def test_delete_task(service, test_user):
    service.create_task("Task to delete", "", test_user.id)
    task = service.list_tasks(test_user.id)[0]

    service.delete_task(task.id, test_user.id)

    tasks = service.list_tasks(test_user.id)
    assert len(tasks) == 0

def test_valid_status_transition(service, test_user):
    service.create_task("Task", "", test_user.id)
    task = service.list_tasks(test_user.id)[0]

    # todo -> doing
    service.change_status(task.id, "doing", test_user.id)
    updated = service.get_task(task.id) 
    assert updated.status == "doing"

    # doing -> done
    service.change_status(task.id, "done", test_user.id)
    updated = service.get_task(task.id)
    assert updated.status == "done"

def test_invalid_transition(service, test_user):
    service.create_task("Task", "", test_user.id)
    task = service.list_tasks(test_user.id)[0]

    # It doesn't allowed todo -> done directly
    with pytest.raises(ValueError):
        service.change_status(task.id, "done", test_user.id)

