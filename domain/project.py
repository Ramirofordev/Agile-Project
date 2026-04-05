from infraestructure.db import db
from datetime import datetime

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    description = db.Column(db.String(250))
    created_at = db.Column(db.Datetime, default = datetime.datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    tasks = db.relationship("Task", backref = "project", lazy = True)

    def __repr__(self):
        return f"<Project {self.name}>"