from domain.task import Task
from infraestructure.db import db

class TaskRepository:
    def add(self, task):
        db.session.add(task)    
        db.session.commit()

    def update(self, task: Task):
        db.session.commit()

    def get_by_id(self, task_id: int):
        return db.session.get(Task, task_id)


    def get_all(self):
        return Task.query.all()