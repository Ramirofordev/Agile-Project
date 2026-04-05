from domain.project import Project
from infraestructure.db import db

class ProjectRepository:
    def add(self, project):
        db.session.add(project)
        db.session.commit()

    def get_by_id(self, project_id):
        return db.session.get(Project, project_id)
    
    def get_all_by_user(self, user_id):
        return Project.query.filter_by(user_id = user_id).all()
    
    def delete(self, project_id):
        project = self.get_by_id(project_id)
        if not project:
            return None
        
        db.session.delete(project)
        db.session.commit()
        return project