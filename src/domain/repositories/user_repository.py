from abc import ABC, abstractmethod
from typing import Optional
from ..entities.user import User
from ..entities.token import Token


class UserRepository(ABC):

    @abstractmethod
    def create_user(
        self, email: str, password: str, alias: Optional[str] = None
    ) -> User:
        pass

    @abstractmethod
    def login_user(self, email: str, password: str) -> Optional[Token]:
        pass

    @abstractmethod
    def get_user(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def update_user(self, user: User) -> User:
        pass

    @abstractmethod
    def send_password_reset_email(self, email: str) -> dict:
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> None:
        pass

    @abstractmethod
    def list_users(self) -> list[User]:
        pass
