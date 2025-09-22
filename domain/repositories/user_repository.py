from abc import ABC, abstractmethod
from typing import List
from domain.entities.user import User

class UserRepository(ABC):
    @abstractmethod
    def add_user(self, user: User) -> None:
        """Add a new user to the repository."""
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> User|None:
        """Retrieve a user by their ID."""
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> User|None:
        """Retrieve a user by their email."""
        pass

    @abstractmethod
    def update_user(self, user: User) -> None:
        """Update an existing user's information."""
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> None:
        """Delete a user from the repository by their ID."""
        pass

    @abstractmethod
    def list_users(self) -> List[User]:
        """List all users in the repository."""
        pass