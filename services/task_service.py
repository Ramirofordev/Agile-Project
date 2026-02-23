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

    def edit_task(self, task_id: int, new_title: str, new_description: str = None):
        task = self.repository.get_by_id(task_id)

        if not task:
            raise ValueError("Task not found")
        
        if not new_title or not new_title.strip():
            raise ValueError("The task must have a title")
        
        task.title = new_title.strip()

        if new_description is not None:
            task.description = new_description

        self.repository.update(task)

        return task
    
    def get_task(self, task_id: int):
         return self.repository.get_by_id(task_id)

    def list_tasks(self):
        return self.repository.get_all()