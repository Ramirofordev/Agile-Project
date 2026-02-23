from domain.task import Task
from infraestructure.db import db

class TaskRepository:
    def add(self, task):
        db.session.add(task)    
        db.session.commit()

    def update(self, task: Task):
        db.session.commit()

    def delete_task(self, task_id):
        task = db.session.get(Task, task_id)
        if not task:
            return None
        
        db.session.delete(task)
        db.session.commit()
        return task

    def update_status(self, task_id, new_status):
        task = db.session.get(Task, task_id)
        if not task:
            return None
        
        task.status = new_status
        db.session.commit()
        
        return task

    def get_by_id(self, task_id: int):
        return db.session.get(Task, task_id)

    def get_all(self):
        return Task.query.all()