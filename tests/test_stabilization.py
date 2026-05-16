import pytest
import requests
from werkzeug.security import generate_password_hash

from app import create_app
from domain.context import Context
from domain.task import Task
from domain.user import User
from infraestructure.db import db
from services.pokemon_services import PokemonService
from services.project_service import ProjectService


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


def create_user(username="user", email="user@test.com"):
    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash("password")
    )
    db.session.add(user)
    db.session.commit()
    return user


def login(client, email):
    return client.post("/login", data={
        "identifier": email,
        "password": "password"
    }, follow_redirects=True)


def test_delete_context_redirects_to_index(app):
    with app.app_context():
        user = create_user()
        context = Context(name="Errands", user_id=user.id)
        db.session.add(context)
        db.session.commit()
        context_id = context.id
        user_email = user.email

    client = app.test_client()
    login(client, user_email)

    response = client.post(f"/contexts/delete/{context_id}")

    assert response.status_code == 302
    assert response.headers["Location"] == "/"


def test_pokemon_service_fallback_creates_typed_pikachu(app, monkeypatch):
    with app.app_context():
        user = create_user()
        service = PokemonService()

        monkeypatch.setattr(service, "generate_shiny", lambda user: False)
        monkeypatch.setattr(service, "get_random_pokemon_data", lambda user, is_shiny: None)
        monkeypatch.setattr(service, "generate_rarity", lambda user_level: "normal")

        pokemon = service.assign_random_pokemon_to_user(user.id, user.level)

        assert pokemon.dex_number == 25
        assert pokemon.name == "pikachu"
        assert pokemon.type1 == "electric"
        assert pokemon.type2 is None


def test_pokemon_service_returns_none_when_pokeapi_request_fails(app, monkeypatch):
    with app.app_context():
        user = create_user()
        service = PokemonService()

        def raise_timeout(url, timeout):
            raise requests.RequestException("PokeAPI unavailable")

        monkeypatch.setattr("services.pokemon_services.requests.get", raise_timeout)

        pokemon_data = service.get_random_pokemon_data(user, is_shiny=False)

        assert pokemon_data is None


def test_pokemon_service_returns_none_when_pokeapi_payload_is_malformed(app, monkeypatch):
    with app.app_context():
        user = create_user()
        service = PokemonService()

        class MalformedResponse:
            status_code = 200

            def json(self):
                return {"sprites": {}}

        monkeypatch.setattr(
            "services.pokemon_services.requests.get",
            lambda url, timeout: MalformedResponse()
        )

        pokemon_data = service.get_random_pokemon_data(user, is_shiny=False)

        assert pokemon_data is None


def test_project_update_persists_after_session_expire(app):
    with app.app_context():
        user = create_user()
        service = ProjectService()
        project = service.create_project("Original", "Before", user.id)

        service.update_project(project.id, "Updated", "After", user.id)
        db.session.expire_all()

        refreshed = service.get_project(project.id, user.id)

        assert refreshed.name == "Updated"
        assert refreshed.description == "After"


def test_edit_task_post_for_another_users_task_redirects(app):
    with app.app_context():
        owner = create_user("owner", "owner@test.com")
        intruder = create_user("intruder", "intruder@test.com")
        task = Task(title="Private", description="Secret", user_id=owner.id)
        db.session.add(task)
        db.session.commit()
        task_id = task.id
        intruder_email = intruder.email

    client = app.test_client()
    login(client, intruder_email)

    response = client.post(f"/edit/{task_id}", data={
        "title": "Hijacked",
        "description": "Nope",
        "priority": "high"
    })

    assert response.status_code == 302
    assert response.headers["Location"] == "/"


def test_edit_task_post_for_missing_task_redirects(app):
    with app.app_context():
        user = create_user()
        user_email = user.email

    client = app.test_client()
    login(client, user_email)

    response = client.post("/edit/999", data={
        "title": "Missing",
        "description": "No task",
        "priority": "low"
    })

    assert response.status_code == 302
    assert response.headers["Location"] == "/"


def test_edit_task_with_invalid_priority_does_not_partially_update(app):
    with app.app_context():
        user = create_user()
        task = Task(title="Original", description="Before", user_id=user.id)
        db.session.add(task)
        db.session.commit()
        task_id = task.id
        user_email = user.email

    client = app.test_client()
    login(client, user_email)

    response = client.post(f"/edit/{task_id}", data={
        "title": "Changed",
        "description": "After",
        "priority": "urgent"
    })

    assert response.status_code == 302
    assert response.headers["Location"] == "/"

    with app.app_context():
        task = db.session.get(Task, task_id)
        assert task.title == "Original"
        assert task.description == "Before"
