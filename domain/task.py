from infraestructure.db import db
from datetime import datetime

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    description = db.Column(db.String(500))
    status = db.Column(db.String(50), default = "todo")
    priority = db.Column(db.String(20), default = "medium")
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    manual_priority = db.Column(db.Boolean, default = False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable = True)

    def __repr__(self):
        return f"<Task {self.title}>"