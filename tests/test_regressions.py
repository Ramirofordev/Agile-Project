from unittest.mock import patch

import requests
from werkzeug.security import generate_password_hash

from app import create_app
from domain.context import Context
from domain.user import User
from infraestructure.db import db
from services.pokemon_services import PokemonService
from services.project_service import ProjectService
from services.task_service import TaskService


def make_app(config = None):
    app = create_app({
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "TESTING": True,
        **(config or {})
    })

    return app


def create_user(username = "trainer", email = "trainer@test.com"):
    user = User(
        username = username,
        email = email,
        password_hash = generate_password_hash("password")
    )
    db.session.add(user)
    db.session.commit()
    return user


def login(client, email = "trainer@test.com"):
    return client.post("/login", data = {
        "identifier": email,
        "password": "password"
    }, follow_redirects = True)


def test_context_delete_route_redirects_to_dashboard():
    app = make_app()

    with app.app_context():
        user = create_user()
        context = Context(name = "Home", user_id = user.id)
        db.session.add(context)
        db.session.commit()
        context_id = context.id

    client = app.test_client()
    login(client)

    response = client.post(
        f"/contexts/delete/{context_id}",
        follow_redirects = False
    )

    assert response.status_code == 302
    assert response.location.endswith("/")


def test_project_update_is_persisted():
    app = make_app()

    with app.app_context():
        user = create_user()
        service = ProjectService()

        project = service.create_project("Old", "", user.id)
        service.update_project(project.id, "New", "Updated", user.id)

        db.session.expire_all()
        updated = service.get_project(project.id, user.id)

        assert updated.name == "New"
        assert updated.description == "Updated"


def test_pokemon_api_failure_uses_complete_fallback():
    app = make_app()

    with app.app_context():
        user = create_user()
        service = PokemonService()

        with patch("services.pokemon_services.requests.get", side_effect = requests.RequestException("down")):
            pokemon = service.assign_random_pokemon_to_user(user.id, user.level)

        assert pokemon.name == "pikachu"
        assert pokemon.type1 == "electric"
        assert pokemon.type2 is None


def test_task_completion_rewards_only_once_after_reopen():
    app = make_app()

    with app.app_context():
        user = create_user()
        service = TaskService()
        task = service.create_task("Finish once", "", user.id)

        with patch("services.task_service.PokemonService.assign_random_pokemon_to_user") as assign:
            assign.return_value = None

            service.change_status(task.id, "doing", user.id)
            service.change_status(task.id, "done", user.id)

            first_xp = user.xp
            first_completed = user.tasks_completed

            service.change_status(task.id, "doing", user.id)
            service.change_status(task.id, "done", user.id)

        assert user.xp == first_xp
        assert user.tasks_completed == first_completed
        assert assign.call_count == 1


def test_api_title_update_preserves_description():
    app = make_app()

    with app.app_context():
        create_user()

    client = app.test_client()
    login(client)

    created = client.post("/api/tasks", json = {
        "title": "Original",
        "description": "Keep me"
    })
    task_id = created.get_json()["id"]

    response = client.put(f"/api/tasks/{task_id}", json = {
        "title": "Updated"
    })

    assert response.status_code == 200
    assert response.get_json()["description"] == "Keep me"


def test_pomodoro_endpoint_is_rate_limited():
    app = make_app({"POMODORO_MIN_SECONDS": 1200})

    with app.app_context():
        create_user()

    client = app.test_client()
    login(client)

    first = client.post("/api/pomodoro/complete")
    second = client.post("/api/pomodoro/complete")

    assert first.status_code == 200
    assert second.status_code == 429
