import pytest
from unittest.mock import Mock
from src.domain.services.user_service import UserService
from src.domain.entities.user import User
from src.domain.entities.token import Token
from src.domain.repositories.user_repository import UserRepository


class TestUserService:
    """Test cases for UserService."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.repository = Mock(spec=UserRepository)
        self.service = UserService(self.repository)

    def test_create_user_success(self):
        """Test creating a new user successfully."""
        # Arrange
        email = "test@example.com"
        password = "password123"
        alias = "testuser"
        expected_user = User(id="user_123", email=email, password=password, alias=alias)

        self.repository.get_user_by_email.return_value = None
        self.repository.create_user.return_value = expected_user

        # Act
        result = self.service.create_user(email, password, alias)

        # Assert
        assert result == expected_user
        self.repository.get_user_by_email.assert_called_once_with(email)
        self.repository.create_user.assert_called_once_with(email, password, alias)

    def test_create_user_already_exists(self):
        """Test creating a user that already exists raises ValueError."""
        # Arrange
        email = "existing@example.com"
        password = "password123"
        existing_user = User(
            id="user_456",
            email=email,
            password="existing_password",
            alias="existing_user",
        )

        self.repository.get_user_by_email.return_value = existing_user

        # Act & Assert
        with pytest.raises(ValueError, match="User with this email already exists"):
            self.service.create_user(email, password)

        self.repository.get_user_by_email.assert_called_once_with(email)
        self.repository.create_user.assert_not_called()

    def test_create_user_without_alias(self):
        """Test creating a user without alias."""
        # Arrange
        email = "test@example.com"
        password = "password123"
        expected_user = User(id="user_123", email=email, password=password, alias=None)

        self.repository.get_user_by_email.return_value = None
        self.repository.create_user.return_value = expected_user

        # Act
        result = self.service.create_user(email, password)

        # Assert
        assert result == expected_user
        self.repository.get_user_by_email.assert_called_once_with(email)
        self.repository.create_user.assert_called_once_with(email, password, None)

    def test_login_user_success(self):
        """Test successful user login."""
        # Arrange
        email = "test@example.com"
        password = "password123"
        existing_user = User(
            id="user_123", email=email, password=password, alias="testuser"
        )
        expected_token = Token(
            local_id="user_123",
            email=email,
            alias="testuser",
            id_token="token_123",
            registered=True,
            refresh_token="refresh_123",
            expires_in="3600",
        )

        self.repository.get_user_by_email.return_value = existing_user
        self.repository.login_user.return_value = expected_token

        # Act
        result = self.service.login_user(email, password)

        # Assert
        assert result == expected_token
        self.repository.get_user_by_email.assert_called_once_with(email)
        self.repository.login_user.assert_called_once_with(email, password)

    def test_login_user_not_found(self):
        """Test login with non-existent user raises ValueError."""
        # Arrange
        email = "nonexistent@example.com"
        password = "password123"

        self.repository.get_user_by_email.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="No user found with this email"):
            self.service.login_user(email, password)

        self.repository.get_user_by_email.assert_called_once_with(email)
        self.repository.login_user.assert_not_called()

    def test_get_user_success(self):
        """Test getting a user by ID successfully."""
        # Arrange
        user_id = "user_123"
        expected_user = User(
            id=user_id,
            email="test@example.com",
            password="password123",
            alias="testuser",
        )

        self.repository.get_user.return_value = expected_user

        # Act
        result = self.service.get_user(user_id)

        # Assert
        assert result == expected_user
        self.repository.get_user.assert_called_once_with(user_id)

    def test_get_user_not_found(self):
        """Test getting a non-existent user returns None."""
        # Arrange
        user_id = "nonexistent_user"

        self.repository.get_user.return_value = None

        # Act
        result = self.service.get_user(user_id)

        # Assert
        assert result is None
        self.repository.get_user.assert_called_once_with(user_id)

    def test_get_user_by_email_success(self):
        """Test getting a user by email successfully."""
        # Arrange
        email = "test@example.com"
        expected_user = User(
            id="user_123", email=email, password="password123", alias="testuser"
        )

        self.repository.get_user_by_email.return_value = expected_user

        # Act
        result = self.service.get_user_by_email(email)

        # Assert
        assert result == expected_user
        self.repository.get_user_by_email.assert_called_once_with(email)

    def test_get_user_by_email_not_found(self):
        """Test getting a non-existent user by email returns None."""
        # Arrange
        email = "nonexistent@example.com"

        self.repository.get_user_by_email.return_value = None

        # Act
        result = self.service.get_user_by_email(email)

        # Assert
        assert result is None
        self.repository.get_user_by_email.assert_called_once_with(email)

    def test_update_user_success(self):
        """Test updating a user successfully."""
        # Arrange
        user = User(
            id="user_123",
            email="updated@example.com",
            password="newpassword123",
            alias="updateduser",
        )
        existing_user = User(
            id="user_123",
            email="old@example.com",
            password="oldpassword",
            alias="olduser",
        )

        self.repository.get_user.return_value = existing_user
        self.repository.get_user_by_email.return_value = None  # Email not in use
        self.repository.update_user.return_value = user

        # Act
        result = self.service.update_user(user)

        # Assert
        assert result == user
        self.repository.get_user.assert_called_once_with(user.id)
        self.repository.get_user_by_email.assert_called_once_with(user.email)
        self.repository.update_user.assert_called_once_with(user)

    def test_update_user_invalid_data(self):
        """Test updating a user with invalid data raises ValueError."""
        # Arrange
        user = User(
            id="user_123",
            email="",  # Invalid email
            password="password123",
            alias="testuser",
        )

        # Act & Assert
        with pytest.raises(ValueError, match="Invalid user data"):
            self.service.update_user(user)

        self.repository.get_user.assert_not_called()
        self.repository.update_user.assert_not_called()

    def test_update_user_not_found(self):
        """Test updating a non-existent user raises ValueError."""
        # Arrange
        user = User(
            id="nonexistent_user",
            email="test@example.com",
            password="password123",
            alias="testuser",
        )

        self.repository.get_user.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="User not found"):
            self.service.update_user(user)

        self.repository.get_user.assert_called_once_with(user.id)
        self.repository.update_user.assert_not_called()

    def test_update_user_email_already_in_use(self):
        """Test updating a user with an email already in use raises ValueError."""
        # Arrange
        user = User(
            id="user_123",
            email="existing@example.com",
            password="password123",
            alias="testuser",
        )
        existing_user = User(
            id="user_123",
            email="old@example.com",
            password="oldpassword",
            alias="olduser",
        )
        other_user = User(
            id="user_456",
            email="existing@example.com",
            password="otherpassword",
            alias="otheruser",
        )

        self.repository.get_user.return_value = existing_user
        self.repository.get_user_by_email.return_value = other_user

        # Act & Assert
        with pytest.raises(ValueError, match="Email already in use"):
            self.service.update_user(user)

        self.repository.get_user.assert_called_once_with(user.id)
        self.repository.get_user_by_email.assert_called_once_with(user.email)
        self.repository.update_user.assert_not_called()

    def test_send_password_reset_email_success(self):
        """Test sending password reset email successfully."""
        # Arrange
        email = "test@example.com"
        existing_user = User(
            id="user_123", email=email, password="password123", alias="testuser"
        )
        expected_result = {"success": True, "message": "Password reset email sent"}

        self.repository.get_user_by_email.return_value = existing_user
        self.repository.send_password_reset_email.return_value = expected_result

        # Act
        result = self.service.send_password_reset_email(email)

        # Assert
        assert result == expected_result
        self.repository.get_user_by_email.assert_called_once_with(email)
        self.repository.send_password_reset_email.assert_called_once_with(email)

    def test_send_password_reset_email_invalid_format(self):
        """Test sending password reset email with invalid email format raises ValueError."""
        # Arrange
        invalid_email = "invalid-email"

        # Act & Assert
        with pytest.raises(ValueError, match="Invalid email format"):
            self.service.send_password_reset_email(invalid_email)

        self.repository.get_user_by_email.assert_not_called()
        self.repository.send_password_reset_email.assert_not_called()

    def test_send_password_reset_email_user_not_found(self):
        """Test sending password reset email for non-existent user raises ValueError."""
        # Arrange
        email = "nonexistent@example.com"

        self.repository.get_user_by_email.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="No user found with this email"):
            self.service.send_password_reset_email(email)

        self.repository.get_user_by_email.assert_called_once_with(email)
        self.repository.send_password_reset_email.assert_not_called()

    def test_delete_user_success(self):
        """Test deleting a user successfully."""
        # Arrange
        user_id = "user_123"
        existing_user = User(
            id=user_id,
            email="test@example.com",
            password="password123",
            alias="testuser",
        )

        self.repository.get_user.return_value = existing_user

        # Act
        self.service.delete_user(user_id)

        # Assert
        self.repository.get_user.assert_called_once_with(user_id)
        self.repository.delete_user.assert_called_once_with(user_id)

    def test_delete_user_not_found(self):
        """Test deleting a non-existent user raises ValueError."""
        # Arrange
        user_id = "nonexistent_user"

        self.repository.get_user.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="User not found"):
            self.service.delete_user(user_id)

        self.repository.get_user.assert_called_once_with(user_id)
        self.repository.delete_user.assert_not_called()

    def test_list_users_success(self):
        """Test listing all users successfully."""
        # Arrange
        expected_users = [
            User(
                id="user_1",
                email="user1@example.com",
                password="password123",
                alias="user1",
            ),
            User(
                id="user_2",
                email="user2@example.com",
                password="password456",
                alias="user2",
            ),
        ]

        self.repository.list_users.return_value = expected_users

        # Act
        result = self.service.list_users()

        # Assert
        assert result == expected_users
        self.repository.list_users.assert_called_once()

    def test_list_users_empty(self):
        """Test listing users when no users exist."""
        # Arrange
        self.repository.list_users.return_value = []

        # Act
        result = self.service.list_users()

        # Assert
        assert result == []
        self.repository.list_users.assert_called_once()
