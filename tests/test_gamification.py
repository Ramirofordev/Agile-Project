import pytest
from app import create_app
from infraestructure.db import db
from domain.user import User
from services.user_progress_services import UserProgressService

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
def progress_service(app):
    return UserProgressService()

@pytest.fixture
def test_user(app):
    user = User(
        username = "trainer",
        email = "trainer@test.com",
        password_hash = "fakehash"
    )

    db.session.add(user)
    db.session.commit()
    
    return user

def test_xp_gain(progress_service, test_user):
    progress_service.add_xp(test_user, 20)

    assert test_user.xp == 20

def test_level_up(progress_service, test_user):

    test_user.xp = 95
    test_user.level = 1

    progress_service.add_xp(test_user, 10)

    assert test_user.level == 2
    assert test_user.xp >= 100

def test_pomodoro_session_increment(progress_service, test_user):

    progress_service.register_pomodoro_completion(test_user)

    assert test_user.pomodoro_sessions_completed == 1

def test_xp_reward_by_priority(progress_service, test_user):

    xp_low = progress_service.register_task_completion(test_user, "low")
    xp_medium = progress_service.register_task_completion(test_user, "medium")
    xp_high = progress_service.register_task_completion(test_user, "high")

    assert xp_low == 10
    assert xp_medium == 20
    assert xp_high == 30

def test_task_completion_with_pomodoro_bonus(progress_service, test_user):

    xp = progress_service.register_task_completion(
        test_user,
        "medium",
        used_pomodoro = True    
    )

    assert xp == 25