from domain.task import Task
from datetime import datetime, timezone
from infraestructure.db import db
from infraestructure.repositories.task_repository import TaskRepository
from services.pokemon_services import PokemonService

class TaskService:
    def __init__(self):
        self.repository = TaskRepository()
        self.pokemon_service = PokemonService()

    def create_task(self, title, description, user_id):
        # Validations
        if not title:
            raise ValueError("The task must have a title")
        
        task = Task(title = title, description = description, user_id = user_id)
        self.repository.add(task)

        return task

    def edit_task(self, task_id: int, new_title: str, user_id: int, new_description: str = None):
        task = self.repository.get_by_id(task_id)

        if not task:
            raise ValueError("Task not found")
        
        if not new_title or not new_title.strip():
            raise ValueError("The task must have a title")
        
        if task.user_id != user_id:
            raise ValueError("Unauthorized action")
        
        task.title = new_title.strip()

        if new_description is not None:
            task.description = new_description

        self.repository.update(task)

        return task
    
    def delete_task(self, task_id: int, user_id: int):
        task = self.repository.get_by_id(task_id)
        
        if not task:
            raise ValueError("Task not found")
        
        if task.user_id != user_id:
            raise ValueError("Unauthorized action")
        
        return self.repository.delete_task(task_id)

    
    def change_status(self, task_id: int, new_status: str, user_id: int):
        task = self.repository.get_by_id(task_id)
        
        if not task:
            raise ValueError("Task not found")
        
        if task.user_id != user_id:
            raise ValueError("Unauthorized action")
        
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
        
        updated_task = self.repository.update_status(task_id, new_status)

        new_pokemon = None

        # If the task it's complete, give the pokemon
        if new_status == "done":
            new_pokemon = self.pokemon_service.assign_random_pokemon_to_user(user_id)

        return updated_task, new_pokemon

    def auto_adjust_priority(self, task):
        if task.manual_priority:
            return # Respect manual override    
        
        days_old = (datetime.utcnow() - task.created_at).days

        if days_old >= 6:
            task.priority = "high"
        elif days_old >= 3:
            task.priority = "medium"
        else:
            task.priority = "low"

    def update_priority(self, task_id, priority, user_id):
        """
        Manually updates task priority
        Overrides automatic priority adjustments.
        """

        task = self.repository.get_by_id(task_id)

        if not task or task.user_id != user_id:
            raise ValueError("Task not found")
        
        if priority not in ["low", "medium", "high"]:
            raise ValueError("Invalid property")
        
        task.priority = priority
        task.manual_priority = True

        db.session.commit()

        return task
            

    def get_task(self, task_id: int):
         return self.repository.get_by_id(task_id)

    def list_tasks(self, user_id):
        tasks = self.repository.get_all_by_user(user_id)

        for task in tasks:
            self.auto_adjust_priority(task)

        db.session.commit()

        return tasks