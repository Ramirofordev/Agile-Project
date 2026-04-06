from domain.context import Context
from infraestructure.repositories.context_repository import ContextRepository

class ContextService:

    def __init__(self):
        self.repository = ContextRepository()

    def create_context(self, name, user_id):
        if not name or not name.strip():
            raise ValueError("Context must have a name")
        
        context = Context(
            name = name.strip(),
            user_id = user_id
        )

        self.repository.add(context)
        return context

    def list_contexts(self, user_id):
        return self.repository.get_all_by_user(user_id)
    
    def delete_context(self, context_id, user_id):
        context = self.repository.get_by_id(context_id)

        if not context or context.user_id != user_id:
            raise ValueError("Context not found")
        
        return self.repository.delete(context_id)