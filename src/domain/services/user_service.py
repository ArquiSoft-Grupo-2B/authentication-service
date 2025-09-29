from typing import Optional, List
from ..entities.user import User
from ..entities.token import Token
from ..repositories.user_repository import UserRepository


class UserService:
    """Service layer for managing users, enforcing business rules."""

    def __init__(self, user_repository: UserRepository):
        """Initialize the service with a user repository of some kind."""
        self.user_repository = user_repository

    def create_user(
        self, email: str, password: str, alias: Optional[str] = None
    ) -> User:
        """Create a new user."""
        # Check if user already exists
        existing_user = self.user_repository.get_user_by_email(email)
        if existing_user:
            raise ValueError("User with this email already exists")

        return self.user_repository.create_user(email, password, alias)

    def login_user(self, email: str, password: str) -> Optional[Token]:
        """Log in a user."""
        existing_user = self.user_repository.get_user_by_email(email)
        if not existing_user:
            raise ValueError("No user found with this email")
        return self.user_repository.login_user(email, password)

    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return self.user_repository.get_user(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.user_repository.get_user_by_email(email)

    def update_user(self, user: User) -> User:
        """Update an existing user after validation."""
        if not user.validate():
            raise ValueError("Invalid user data")
        existing_user = self.user_repository.get_user(user.id)
        if not existing_user:
            raise ValueError("User not found")
        if (
            existing_user.email != user.email
            and self.user_repository.get_user_by_email(user.email)
        ):
            raise ValueError("Email already in use")

        return self.user_repository.update_user(user)

    def send_password_reset_email(self, email: str) -> dict:
        """Send a password reset email."""
        return self.user_repository.send_password_reset_email(email)

    def delete_user(self, user_id: str) -> None:
        """Delete a user by ID."""
        existing_user = self.user_repository.get_user(user_id)
        if not existing_user:
            raise ValueError("User not found")

        self.user_repository.delete_user(user_id)

    def list_users(self) -> List[User]:
        """List all users."""
        return self.user_repository.list_users()
