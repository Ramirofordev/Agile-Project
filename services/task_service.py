from domain.task import Task

class TaskService:
    def __init__(self, repository):
        self.repository = repository

    def create_task(self, title, description):
        # Validations
        if not title:
            raise ValueError("The task must have a title")
        
        task = Task(title, description)

    def list_tasks(self):
        return self.repository.get_all()