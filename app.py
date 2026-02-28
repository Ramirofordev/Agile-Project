from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from infraestructure.db import db
from services.task_service import TaskService
from services.auth_service import AuthService
from infraestructure.repositories.user_repository import UserRepository
from domain.user import User


def create_app(test_config=None):

    app = Flask(__name__)

    app.config["SECRET_KEY"] = "super_secret_key_for_dev"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config:
        app.config.update(test_config)
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///kanban.db"

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.init_app(app)

    task_service = TaskService()
    auth_service = AuthService(UserRepository())

    # -------------------------
    # Flask-Login loader
    # -------------------------

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # -------------------------
    # Routes
    # -------------------------

    @app.route("/")
    @login_required
    def index():
        tasks = task_service.list_tasks(current_user.id)
        return render_template("board.html", tasks=tasks)

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

        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            try:
                user = auth_service.authenticate_user(
                    request.form["email"],
                    request.form["password"]
                )
                login_user(user)
                return redirect(url_for("index"))
            except ValueError as e:
                flash(str(e), "danger")
                return redirect(url_for("login"))

        return render_template("login.html")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("login"))

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

        return render_template("edit.html", task=task)

    @app.route("/edit/<int:task_id>", methods=["POST"])
    @login_required
    def edit_task(task_id):
        try:
            task_service.edit_task(
                task_id,
                request.form["title"],
                current_user.id,
                request.form.get("description", "")
            )
        except ValueError as e:
            flash(str(e), "danger")

        return redirect(url_for("index"))

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

    @app.route("/status/<int:task_id>/<new_status>", methods=["POST"])
    @login_required
    def change_status(task_id, new_status):
        try:
            task_service.change_status(task_id, new_status, current_user.id)
            return "", 204
        except ValueError:
            return "", 400

    return app


# -------------------------
# Run App
# -------------------------

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)