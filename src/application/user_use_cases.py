from ..domain.entities.user import User
from ..domain.repositories.user_repository import UserRepository
from ..utils.validators import validate_email


class UserUseCases:
    """Use cases for managing users, coordinating between service and repository layers."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, email: str, password: str, alias: str | None = None) -> dict:
        """Create a new user."""
        existing_user = self.user_repository.get_user_by_email(email)
        if existing_user:
            raise ValueError("User with this email already exists")

        created_user = self.user_repository.create_user(email, password, alias)
        return created_user.to_dict_no_password()

    def login_user(self, email: str, password: str) -> dict | None:
        """Log in a user."""
        existing_user = self.user_repository.get_user_by_email(email)
        if not existing_user:
            raise ValueError("No user found with this email")

        logged_user = self.user_repository.login_user(email, password)
        return logged_user.to_dict() if logged_user else None

    def get_user(self, user_id: str) -> dict | None:
        user = self.user_repository.get_user(user_id)
        return user.to_dict_no_password() if user else None

    def get_user_by_email(self, email: str) -> User | None:
        """Get user by email."""
        return self.user_repository.get_user_by_email(email)

    def update_user(self, user_data: dict) -> None:
        """Update an existing user after validation."""
        user = User(**user_data)
        not_password = user.password is None
        not_alias = user.alias is None

        if not user.validate(
            exclude_password=not_password, exclude_alias=not_alias
        ):  # Exclude password and alias from validation
            raise ValueError("Invalid user data")
        existing_user = self.user_repository.get_user(user.id)
        if not existing_user:
            raise ValueError("User not found")
        if (
            existing_user.email != user.email
            and self.user_repository.get_user_by_email(user.email)
        ):
            raise ValueError("Email already in use")

        updated_user = self.user_repository.update_user(user)

        return updated_user.to_dict_no_password() if updated_user else None

    def send_password_reset_email(self, email: str) -> dict:
        if not validate_email(email):
            raise ValueError("Invalid email format")
        if not self.user_repository.get_user_by_email(email):
            raise ValueError("No user found with this email")

        return self.user_repository.send_password_reset_email(email)

    def delete_user(self, user_id: str) -> None:
        """Delete a user by ID."""
        existing_user = self.user_repository.get_user(user_id)
        if not existing_user:
            raise ValueError("User not found")

        self.user_repository.delete_user(user_id)

    def list_users(self) -> list[dict]:
        users = self.user_repository.list_users()
        return [user.to_dict_no_password() for user in users]
