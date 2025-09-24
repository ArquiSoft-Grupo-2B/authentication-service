from typing import Dict, Optional
from ...domain.repositories.user_repository import UserRepository
from ...domain.entities.user import User


class InMemoryUserRepository(UserRepository):
    """In-memory implementation of UserRepository for testing purposes."""

    def __init__(self):
        self.users: Dict[str, User] = {}
        self.counter = 1

    def create_user(
        self, email: str, password: str, alias: Optional[str] = None
    ) -> User:
        """Create a new user and return it."""
        user = User(id=str(self.counter), password=password, email=email, alias=alias)
        self.counter += 1
        self.users[user.id] = user
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return self.users.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    def update_user(self, user: User) -> User:
        """Update an existing user."""
        if user.id not in self.users:
            raise ValueError("User not found")
        self.users[user.id] = user
        return user

    def delete_user(self, user_id: str) -> None:
        """Delete user by ID."""
        if user_id not in self.users:
            raise ValueError("User not found")
        del self.users[user_id]

    def list_users(self):
        return self.users.values()
