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
    
    def delete_task(self, task_id: int):
        task = self.repository.get_by_id(task_id)
        
        if not task:
            raise ValueError("Task not found")
        
        return self.repository.delete_task(task_id)

    
    def change_status(self, task_id: int, new_status: str):
        task = self.repository.get_by_id(task_id)
        
        if not task:
            raise ValueError("Task not found")
        
        allowed_transitions = {
            "todo": ["doing"],
            "doing": ["done"],
            "done": {"doing"}
        }

        current_status = task.status

        if new_status not in allowed_transitions[current_status]:
            raise ValueError(
                f"Invalid transition from {current_status} to {new_status}"
            )
        
        return self.repository.update_status(task_id, new_status)
    
    def get_task(self, task_id: int):
         return self.repository.get_by_id(task_id)

    def list_tasks(self):
        return self.repository.get_all()