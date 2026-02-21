from infraestructure.db import db

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    description = db.Column(db.String(500))
    status = db.Column(db.String(50), default = "todo")

    def __repr__(self):
        return f"<Task {self.title}>"