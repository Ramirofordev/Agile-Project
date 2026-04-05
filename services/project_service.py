from domain.project import Project
from infraestructure.repositories.project_repository import ProjectRepository

class ProjectService:
    def __init__(self):
        self.repository = ProjectRepository()

    def create_project(self, name, description, user_id):
        if not name or not name.strip():
            raise ValueError("Project must have a name")
        
        project = Project(
            name = name.strip(),
            description = description,
            user_id = user_id
        )

        self.repository.add(project)
        return project
    
    def list_projects(self, user_id):
        return self.repository.get_all_by_user(user_id)
    
    def get_project(self, project_id, user_id):
        project = self.repository.get_by_id(project_id)

        if not project or project.user_id != user_id:
            raise ValueError("Project not found")
        
        return project