from abc import ABC, abstractmethod
from typing import Optional
from ..entities.user import User


class UserRepository(ABC):

    @abstractmethod
    def create(
        self, email: str, password: str, display_name: Optional[str] = None
    ) -> User:
        pass

    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        pass

    @abstractmethod
    def delete(self, user_id: str) -> None:
        pass
