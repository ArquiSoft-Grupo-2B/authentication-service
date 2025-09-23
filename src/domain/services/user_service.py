from typing import Optional, List
from ..entities.user import User
from ..repositories.user_repository import UserRepository


class UserService:
    """Service layer for managing users, enforcing business rules."""

    def __init__(self, user_repository: UserRepository):
        """Initialize the service with a user repository of some kind."""
        self.user_repository = user_repository

    def create_user(
        self, email: str, password: str, display_name: Optional[str] = None
    ) -> User:
        """Create a new user."""
        # Check if user already exists
        existing_user = self.user_repository.find_by_email(email)
        if existing_user:
            raise ValueError("User with this email already exists")

        return self.user_repository.create(email, password, display_name)

    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return self.user_repository.find_by_id(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.user_repository.find_by_email(email)

    def update_user(self, user: User) -> User:
        """Update an existing user after validation."""
        if not user.validate():
            raise ValueError("Invalid user data")
        existing_user = self.user_repository.find_by_id(user.id)
        if not existing_user:
            raise ValueError("User not found")
        if existing_user.email != user.email and self.user_repository.find_by_email(
            user.email
        ):
            raise ValueError("Email already in use")

        return self.user_repository.update(user)

    def delete_user(self, user_id: str) -> None:
        """Delete a user by ID."""
        existing_user = self.user_repository.find_by_id(user_id)
        if not existing_user:
            raise ValueError("User not found")

        self.user_repository.delete(user_id)
