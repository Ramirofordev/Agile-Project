from domain.task import Task
from infraestructure.db import db

class TaskRepository:
    def add(self, task):
        db.session.add(task)    
        db.session.commit()

    def get_all(self):
        return Task.query.all()