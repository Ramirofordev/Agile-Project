from werkzeug.security import generate_password_hash, check_password_hash
from infraestructure.repositories.user_repository import UserRepository
from domain.user import User

class AuthService:
    def __init__(self, user_repository = None):
        self.user_repository = user_repository or UserRepository()

    def register_user(self, username: str, email: str, password: str):
        if not username or not email or not password:
            raise ValueError("All fields are required")
        
        if self.user_repository.get_by_email(email):
            raise ValueError("Email already registered")
        
        if self.user_repository.get_by_username(username):
            raise ValueError("Username already taken")
        
        password_hash = generate_password_hash(password)

        user = User(
            username = username.strip(),
            email = email.strip(),
            password_hash = password_hash
        )

        self.user_repository.add(user)

        return user

    def authenticate_user(self, email: str, password: str):

        email = email.strip()
        
        user = self.user_repository.get_by_email(email)

        if not user:
            raise ValueError("Invalid credentials")
        
        if not check_password_hash(user.password_hash, password):
            raise ValueError("Invalid credentials")
        
        print("User found:", user)
        print("Password hash:", user.password_hash if user else None)
        
        return user