from domain.entities.user import User
from domain.repositories.user_repository import UserRepository


class UserService:
    """Service layer for managing users, enforcing business rules."""

    def __init__(self, user_repository: UserRepository):
        """Initialize the service with a user repository of some kind."""
        self.user_repository = user_repository

    def get_user(self, user_id: str) -> User | None:
        return self.user_repository.get_user_by_id(user_id)

    def validate_user_for_update(self, user: User) -> None:
        if not user.validate():
            raise ValueError("Invalid user data")
        existing_user = self.user_repository.get_user_by_id(user.id)
        if not existing_user:
            raise ValueError("User not found")
        if (
            existing_user.email != user.email
            and self.user_repository.get_user_by_email(user.email)
        ):
            raise ValueError("Email already in use")

    def list_users(self) -> list[User]:
        return self.user_repository.list_users()
