from domain.task import Task
from infraestructure.repositories.task_repository import TaskRepository

class TaskService:
    def __init__(self):
        self.repository = TaskRepository()

    def create_task(self, title, description):
        # Validations
        if not title:
            raise ValueError("The task must have a title")
        
        task = Task(title = title, description = description)
        self.repository.add(task)

    def list_tasks(self):
        return self.repository.get_all()