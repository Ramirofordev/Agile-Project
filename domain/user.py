from infraestructure.db import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), nullable = False, unique = True)
    email = db.Column(db.String(150), nullable = False, unique = True)
    password_hash = db.Column(db.String(255), nullable = False)

    xp = db.Column(db.Integer, default = 0)
    level = db.Column(db.Integer, default = 1)
    pomodoro_sessions_completed = db.Column(db.Integer, default = 0)
    tasks_completed = db.Column(db.Integer, default = 0)

    tasks = db.relationship("Task", backref= "owner", lazy = True)
    pokemons = db.relationship("Pokemon", backref = "owner", lazy = True)

    def __repr__(self):
        return f"<User {self.username}>"