from domain.context import Context
from infraestructure.db import db

class ContextRepository:

    def add(self, context):
        db.session.add(context)
        db.session.commit()

    def get_by_id(self, context_id):
        return db.session.get(Context, context_id)
    
    def get_all_by_user(self, user_id):
        return Context.query.filter_by(user_id = user_id).all()
    
    def delete(self, context_id):
        context = self.get_by_id(context_id)
        if not context:
            return None
        
        db.session.delete(context)
        db.session.commit()
        return context