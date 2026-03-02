import pytest
from unittest.mock import patch
from app import create_app
from infraestructure.db import db
from services.task_service import TaskService
from domain.user import User

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
def service(app):
    return TaskService()

@pytest.fixture
def test_user(app):
    user = User(
        username = "pokeuser",
        email = "poke@test.com",
        password_hash = "fakehash"
    )

    db.session.add(user)
    db.session.commit()

    return user


def test_pokemon_reward_on_done(service, test_user):
    task = service.create_task("Catch me", "", test_user.id)

    with patch("services.task_service.PokemonService.assign_random_pokemon_to_user") as mock_assing:

        mock_assing.return_value = type("Pokemon", (), {
            "name": "pikachu",
            "sprite_url": "sprite.png"
        })()

        # todo -> doing
        service.change_status(task.id, "doing", test_user.id)

        # doing -> done
        updated_task, pokemon = service.change_status(task.id, "done", test_user.id)

        assert pokemon is not None  
        assert pokemon.name == "pikachu"    