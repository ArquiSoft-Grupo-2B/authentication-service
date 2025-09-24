from ..domain.services.user_service import UserService
from ..domain.entities.user import User
from ..domain.repositories.user_repository import UserRepository


class UserUseCases:
    """Use cases for managing users, coordinating between service and repository layers."""

    def __init__(self, user_repository: UserRepository):
        self.user_service = UserService(user_repository)

    def create_user(self, email: str, password: str, alias: str | None = None) -> dict:
        user = self.user_service.create_user(email, password, alias)
        return user

    def get_user(self, user_id: str) -> dict | None:
        user = self.user_service.get_user(user_id)
        return user if user else None

    def update_user(self, user_data: dict) -> None:
        user = User(**user_data)
        user = self.user_service.update_user(user)
        return user

    def delete_user(self, user_id: str) -> None:
        self.user_service.delete_user(user_id)

    def list_users(self) -> list[dict]:
        users = self.user_service.list_users()
        return [user.to_dict_no_password() for user in users]
