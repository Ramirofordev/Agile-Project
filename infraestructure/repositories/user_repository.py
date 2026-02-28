from domain.user import User
from infraestructure.db import db   

class UserRepository:

    def add(self, user):
        db.session.add(user)
        db.session.commit()

    def get_by_email(self, email: str):
        return User.query.filter_by(email = email).first()
    
    def get_by_id(self, user_id: int):
        return db.session.get(User, user_id)
    
    def get_by_username(self, username: str):
        return User.query.filter_by(username = username).first()