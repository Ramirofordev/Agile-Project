from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from infraestructure.db import db
from services.task_service import TaskService
from services.auth_service import AuthService
from services.user_progress_services import UserProgressService
from services.profile_service import ProfileService
from services.project_service import ProjectService
from infraestructure.repositories.user_repository import UserRepository
from domain.user import User

import os


def create_app(test_config=None):

    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev_key")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config:
        app.config.update(test_config)
    else:
        db_path = os.path.join(os.getcwd(), "kanban.db")
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.init_app(app)

    task_service = TaskService()
    auth_service = AuthService(UserRepository())
    user_progress_service = UserProgressService()
    profile_service = ProfileService()
    project_service = ProjectService()

    # -------------------------
    # Flask-Login loader
    # -------------------------

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # -------------------------
    # Routes
    # -------------------------

    @app.route("/")
    @login_required
    def index():
        tasks = task_service.list_tasks(current_user.id)
        return render_template("pages/dashboard.html", tasks=tasks, user = current_user)

    @app.route("/profile")
    @login_required
    def profile():

        pokedex = profile_service.build_pokedex(current_user)

        stats = profile_service.get_profile_stats(current_user)

        achievements = profile_service.get_achievements(stats)

        return render_template(
            "pages/profile.html",
            user = current_user,
            pokedex = pokedex,
            captured = stats["captured"],
            percent = stats["percent"],
            shinies = stats["shinies"],
            legendary = stats["legendary"],
            total_pokemon = profile_service.TOTAL_POKEMON,
            achievements = achievements
        )

    # -------------------------
    # Authentication
    # -------------------------

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            try:
                user = auth_service.register_user(
                    request.form["username"],
                    request.form["email"],
                    request.form["password"]
                )
                login_user(user)
                return redirect(url_for("index"))
            except ValueError as e:
                flash(str(e), "danger")
                return redirect(url_for("register"))

        return render_template("pages/register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            try:
                user = auth_service.authenticate_user(
                    request.form["identifier"],
                    request.form["password"]
                )
                login_user(user)
                return redirect(url_for("index"))
            except ValueError as e:
                flash(str(e), "danger")
                return redirect(url_for("login"))

        return render_template("pages/login.html")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("login"))
    
    # -------------------------
    # Project
    # -------------------------
    
    @app.route("/projects", methods = ["GET"])
    @login_required
    def list_projects():
        projects = project_service.list_projects(current_user.id)
        return render_template("pages/projects.html", projects = projects)
    
    @app.route("/projects", methods = ["POST"])
    @login_required
    def create_project():
        try:
            project_service.create_project(
                request.form["name"],
                request.form.get("description", ""),
                current_user.id
            )
        except ValueError as e:
            flash(str(e), "danger")

        return redirect(url_for("list_projects"))
    
    @app.route
    @login_required
    def view_project(project_id):
        try:
            project = project_service.get_project(project_id, current_user.id)
            return render_template("pages/product_detail.html", project = project)
        except ValueError:
            return redirect(url_for("lists_projects"))

    # -------------------------
    # Task CRUD
    # -------------------------

    @app.route("/add", methods=["POST"])
    @login_required
    def add_task():
        try:
            task_service.create_task(
                request.form["title"],
                request.form.get("description", ""),
                current_user.id
            )
        except ValueError as e:
            flash(str(e), "danger")

        return redirect(url_for("index"))

    @app.route("/edit/<int:task_id>", methods=["GET"])
    @login_required
    def edit_task_form(task_id):
        task = task_service.get_task(task_id)

        if not task or task.user_id != current_user.id:
            return redirect(url_for("index"))

        return render_template("pages/edit.html", task=task)

    @app.route("/edit/<int:task_id>", methods=["POST"])
    @login_required
    def edit_task(task_id):
        task = task_service.get_task(task_id)

        if request.method == "POST":

            title = request.form["title"]
            description = request.form["description"]
            priority = request.form["priority"]

            task_service.edit_task(
                task_id,
                title,
                current_user.id,
                description
            )

            task_service.update_priority(
                task_id,
                priority,
                current_user.id
            )

            return redirect(url_for("index"))

        return render_template("pages/edit.html", task = task)

    @app.route("/delete/<int:task_id>", methods=["POST"])
    @login_required
    def delete_task(task_id):
        try:
            task_service.delete_task(task_id, current_user.id)
        except ValueError:
            pass

        return redirect(url_for("index"))

    # -------------------------
    # Drag & Drop Status Change
    # -------------------------

    @app.route("/status/<int:task_id>/<new_status>", methods = ["POST"])
    @login_required
    def change_status(task_id, new_status):
        try:
            data = request.get_json(silent = True) or {}
            used_pomodoro = data.get("used_pomodoro", False)

            _, new_pokemon = task_service.change_status(task_id, new_status, current_user.id, used_pomodoro)

            if new_pokemon:
                return jsonify({
                    "pokemon_name": new_pokemon.name,
                    "pokemon_sprite": new_pokemon.sprite_url,
                    "pokemon_id": new_pokemon.dex_number,
                    "is_shiny": new_pokemon.is_shiny,
                    "total_xp": current_user.xp,
                    "level": current_user.level,
                    "next_level_xp": user_progress_service.xp_needed_for_next_level(current_user.level)
                }), 200
            
            return jsonify({
                "total_xp": current_user.xp,
                "level": current_user.level,
                "next_level_xp": user_progress_service.xp_needed_for_next_level(current_user.level)
            })

        except ValueError:
            return "", 400
        
    @app.route("/api/pomodoro/complete", methods = ["POST"])
    @login_required
    def complete_pomodoro():
        xp_gained = user_progress_service.register_pomodoro_completion(current_user)

        return jsonify({
            "xp_gained": xp_gained,
            "total_xp": current_user.xp,
            "level": current_user.level,
            "next_level_xp": user_progress_service.xp_needed_for_next_level(current_user.level)
        })
        
    # ----------------------
    # REST API
    # ----------------------

    @app.route("/api/tasks", methods = ["GET"])
    @login_required
    def api_list_tasks():
        tasks = task_service.list_tasks(current_user.id)

        return jsonify([
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status
            }
            for task in tasks
        ])
    
    @app.route("/api/tasks/<int:task_id>", methods = ["GET"])
    @login_required
    def api_get_task(task_id):
        task = task_service.get_task(task_id)

        if not task or task.user_id != current_user.id:
            return jsonify({"error": "Task not found"}), 404
        
        return jsonify({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status
        })
    
    @app.route("/api/tasks", methods = ["POST"])
    @login_required
    def api_create_task():
        data = request.get_json()

        if not data or "title" not in data:
            return jsonify({"error": "Title is required"}), 400
        
        try:
            task = task_service.create_task(
                data["title"],
                data.get("description", ""),
                current_user.id
            )

            return jsonify({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status
            }), 201
        
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        
    @app.route("/api/tasks/<int:task_id>", methods = ["PUT"])
    @login_required
    def api_update_task(task_id):
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
        
        try:
            if "status" in data:
                _, _ = task_service.change_status(
                    task_id,
                    data["status"],
                    current_user.id
                )
            
            if "priority" in data:
                task_service.update_priority(
                    task_id,
                    data["priority"],
                    current_user.id
                )

            if "title" in data:
                task_service.edit_task(
                    task_id,
                    data["title"],
                    current_user.id,
                    data.get("description", "")
                )
                

            task = task_service.get_task(task_id)
            
            return jsonify({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status
            })
        
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        
    @app.route("/api/tasks/<int:task_id>", methods = ["DELETE"])
    @login_required
    def api_delete_task(task_id):
        try:
            task_service.delete_task(task_id, current_user.id)
            return "", 204
        except ValueError:
            return jsonify({"error": "Task not found"}), 404
        
    with app.app_context():
        db.create_all()

    return app

# -------------------------
# Run App
# -------------------------

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host = "0.0.0.0",
        port = port,
        debug = False
    )