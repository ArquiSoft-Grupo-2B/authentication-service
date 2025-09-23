from typing import Dict, List, Optional
from ...domain.repositories.user_repository import UserRepository
from ...domain.entities.user import User


class InMemoryUserRepository(UserRepository):
    """In-memory implementation of UserRepository for testing purposes."""

    def __init__(self):
        self.users: Dict[str, User] = {}
        self.counter = 1

    def create_user(self, user: User) -> User:
        """Create a new user and return it."""
        if not user.id:
            user.id = str(self.counter)
            self.counter += 1
        self.users[user.id] = user
        return user

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return self.users.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    def update_user(self, user: User) -> Optional[User]:
        """Update an existing user."""
        if user.id in self.users:
            self.users[user.id] = user
            return user
        return None

    def delete_user(self, user_id: str) -> bool:
        """Delete user by ID. Returns True if deleted, False if not found."""
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
