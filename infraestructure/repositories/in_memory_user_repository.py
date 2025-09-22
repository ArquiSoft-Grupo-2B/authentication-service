from typing import Dict, List, Optional
from ...domain.repositories.user_repository import UserRepository
from ...domain.entities.user import User


class InMemoryUserRepository(UserRepository):
    """In-memory implementation of UserRepository for testing purposes."""

    def __init__(self):
        self.users: Dict[str, User] = {}
        self.counter = 1

    def get_user_by_id(self, user_id: str) -> User | None:
        return self.users.get(user_id)

    def get_user_by_email(self, email: str) -> User | None:
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    def update_user(self, user: User) -> User | None:
        if user.id in self.users:
            self.users[user.id] = user
            return user
        return None

    def list_users(self) -> list[User]:
        return list(self.users.values())
