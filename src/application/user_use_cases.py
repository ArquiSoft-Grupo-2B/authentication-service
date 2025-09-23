from ..domain.services.user_service import UserService
from ..domain.entities.user import User
from ..domain.repositories.user_repository import UserRepository


class UserUseCases:
    """Use cases for managing users, coordinating between service and repository layers."""

    def __init__(self, user_repository: UserRepository):
        self.user_service = UserService(user_repository)

    def get_user(self, user_id: str) -> dict | None:
        user = self.user_service.get_user(user_id)
        return user.to_dict_no_password() if user else None

    def update_user(self, user_data: dict) -> None:
        user = User(**user_data)
        self.user_service.validate_user_for_update(user)
        self.user_service.user_repository.update_user(user)

    def list_users(self) -> list[dict]:
        users = self.user_service.list_users()
        return [user.to_dict_no_password() for user in users]
