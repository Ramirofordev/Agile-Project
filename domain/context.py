from infraestructure.db import db

class Context(db.Model):
    __tablename__ = "contexts"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)

    tasks = db.relationship("Task", backref = "context", lazy = True)

    def __repr__(self):
        return f"<Context {self.name}>"