from flask import Flask, render_template, request, redirect, url_for
from infraestructure.db import db
from services.task_service import TaskService

task_service = TaskService()

def create_app(test_config = None):
    app = Flask(__name__)

    if test_config:
        app.config.update(test_config)
    else:  
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///kanban.db"
        
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        from domain.task import Task
        db.create_all()

    return app

app = create_app()

@app.route("/")
def index():
    tasks = task_service.list_tasks()
    return render_template("index.html", tasks = tasks)

@app.route("/add", methods = ["POST"])
def add_task():
    title = request.form["title"]
    description = request.form["description"]

    task_service.create_task(title, description)

    return redirect(url_for("index"))

@app.route("/edit/<int:task_id>")
def edit_task_form(task_id):
    task = task_service.get_task(task_id)

    if not task:
        return redirect(url_for("index"))
    
    return render_template("edit.html", task = task)

@app.route("/edit/<int:task_id>", methods = ["POST"])
def edit_task(task_id):
    title = request.form["title"]
    description = request.form["description"]

    task_service.edit_task(task_id, title, description)

    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>", methods = ["POST"])
def delete_task(task_id):
    task_service.delete_task(task_id)
    return redirect(url_for("index"))

@app.route("/status/<int:task_id>/<string:new_status>", methods = ["POST"])
def change_status(task_id, new_status):
    task_service.change_status(task_id, new_status)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug = True)