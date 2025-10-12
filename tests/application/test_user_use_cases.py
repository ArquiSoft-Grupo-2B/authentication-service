import pytest
from unittest.mock import Mock
from src.application.user_use_cases import UserUseCases
from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository


class TestUserUseCases:
    """Test cases for UserUseCases."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.repository = Mock(spec=UserRepository)
        self.use_cases = UserUseCases(self.repository)

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
        result = self.use_cases.create_user(email, password, alias)

        # Assert
        assert result == expected_user.to_dict_no_password()
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
            self.use_cases.create_user(email, password)

        self.repository.get_user_by_email.assert_called_once_with(email)
        self.repository.create_user.assert_not_called()

    def test_login_user_success(self):
        """Test logging in a user successfully."""
        # Arrange
        email = "test@example.com"
        password = "password123"
        expected_user = User(
            id="user_123",
            email=email,
            password=password,
            alias="testuser",
        )

        self.repository.get_user_by_email.return_value = expected_user
        self.repository.login_user.return_value = expected_user

        # Act
        result = self.use_cases.login_user(email, password)

        # Assert
        assert result == expected_user.to_dict_no_password()
        self.repository.get_user_by_email.assert_called_once_with(email)
        self.repository.login_user.assert_called_once_with(email, password)

    def test_login_user_not_found(self):
        """Test logging in a user that doesn't exist raises ValueError."""
        # Arrange
        email = "nonexistent@example.com"
        password = "password123"

        self.repository.get_user_by_email.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="No user found with this email"):
            self.use_cases.login_user(email, password)

        self.repository.get_user_by_email.assert_called_once_with(email)
        self.repository.login_user.assert_not_called()

    def test_login_user_invalid_credentials(self):
        """Test logging in with invalid credentials returns None."""
        # Arrange
        email = "test@example.com"
        password = "wrong_password"
        existing_user = User(
            id="user_123",
            email=email,
            password="correct_password",
            alias="testuser",
        )

        self.repository.get_user_by_email.return_value = existing_user
        self.repository.login_user.return_value = None

        # Act
        result = self.use_cases.login_user(email, password)

        # Assert
        assert result is None
        self.repository.get_user_by_email.assert_called_once_with(email)
        self.repository.login_user.assert_called_once_with(email, password)

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
        result = self.use_cases.get_user(user_id)

        # Assert
        assert result == expected_user.to_dict_no_password()
        self.repository.get_user.assert_called_once_with(user_id)

    def test_get_user_not_found(self):
        """Test getting a user that doesn't exist returns None."""
        # Arrange
        user_id = "nonexistent_user"
        self.repository.get_user.return_value = None

        # Act
        result = self.use_cases.get_user(user_id)

        # Assert
        assert result is None
        self.repository.get_user.assert_called_once_with(user_id)

    def test_get_user_by_email_success(self):
        """Test getting a user by email successfully."""
        # Arrange
        email = "test@example.com"
        expected_user = User(
            id="user_123",
            email=email,
            password="password123",
            alias="testuser",
        )

        self.repository.get_user_by_email.return_value = expected_user

        # Act
        result = self.use_cases.get_user_by_email(email)

        # Assert
        assert result == expected_user
        self.repository.get_user_by_email.assert_called_once_with(email)

    def test_update_user_success(self):
        """Test updating a user successfully."""
        # Arrange
        user_data = {
            "id": "user_123",
            "email": "updated@example.com",
            "alias": "updated_user",
        }
        existing_user = User(
            id="user_123",
            email="old@example.com",
            password="password123",
            alias="old_user",
        )
        updated_user = User(
            id="user_123",
            email="updated@example.com",
            password="password123",
            alias="updated_user",
        )

        self.repository.get_user.return_value = existing_user
        self.repository.get_user_by_email.return_value = None
        self.repository.update_user.return_value = updated_user

        # Act
        result = self.use_cases.update_user(user_data)

        # Assert
        assert result == updated_user.to_dict_no_password()
        self.repository.get_user.assert_called_once_with("user_123")
        self.repository.update_user.assert_called_once()

    def test_update_user_not_found(self):
        """Test updating a user that doesn't exist raises ValueError."""
        # Arrange
        user_data = {
            "id": "nonexistent_user",
            "email": "test@example.com",
            "alias": "testuser",
        }

        self.repository.get_user.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="User not found"):
            self.use_cases.update_user(user_data)

        self.repository.get_user.assert_called_once_with("nonexistent_user")
        self.repository.update_user.assert_not_called()

    def test_update_user_email_already_in_use(self):
        """Test updating a user with an email already in use raises ValueError."""
        # Arrange
        user_data = {
            "id": "user_123",
            "email": "taken@example.com",
            "alias": "updated_user",
        }
        existing_user = User(
            id="user_123",
            email="old@example.com",
            password="password123",
            alias="old_user",
        )
        other_user = User(
            id="user_456",
            email="taken@example.com",
            password="password456",
            alias="other_user",
        )

        self.repository.get_user.return_value = existing_user
        self.repository.get_user_by_email.return_value = other_user

        # Act & Assert
        with pytest.raises(ValueError, match="Email already in use"):
            self.use_cases.update_user(user_data)

        self.repository.get_user.assert_called_once_with("user_123")
        self.repository.update_user.assert_not_called()

    def test_send_password_reset_email_success(self):
        """Test sending password reset email successfully."""
        # Arrange
        email = "test@example.com"
        expected_user = User(
            id="user_123",
            email=email,
            password="password123",
            alias="testuser",
        )
        expected_result = {"message": "Password reset email sent"}

        self.repository.get_user_by_email.return_value = expected_user
        self.repository.send_password_reset_email.return_value = expected_result

        # Act
        result = self.use_cases.send_password_reset_email(email)

        # Assert
        assert result == expected_result
        self.repository.get_user_by_email.assert_called_once_with(email)
        self.repository.send_password_reset_email.assert_called_once_with(email)

    def test_send_password_reset_email_invalid_format(self):
        """Test sending password reset email with invalid format raises ValueError."""
        # Arrange
        invalid_email = "invalid-email"

        # Act & Assert
        with pytest.raises(ValueError, match="Invalid email format"):
            self.use_cases.send_password_reset_email(invalid_email)

        self.repository.get_user_by_email.assert_not_called()
        self.repository.send_password_reset_email.assert_not_called()

    def test_send_password_reset_email_user_not_found(self):
        """Test sending password reset email for non-existent user raises ValueError."""
        # Arrange
        email = "nonexistent@example.com"
        self.repository.get_user_by_email.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="No user found with this email"):
            self.use_cases.send_password_reset_email(email)

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
        self.use_cases.delete_user(user_id)

        # Assert
        self.repository.get_user.assert_called_once_with(user_id)
        self.repository.delete_user.assert_called_once_with(user_id)

    def test_delete_user_not_found(self):
        """Test deleting a user that doesn't exist raises ValueError."""
        # Arrange
        user_id = "nonexistent_user"
        self.repository.get_user.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="User not found"):
            self.use_cases.delete_user(user_id)

        self.repository.get_user.assert_called_once_with(user_id)
        self.repository.delete_user.assert_not_called()

    def test_list_users_success(self):
        """Test listing all users successfully."""
        # Arrange
        users = [
            User(
                id="user_1",
                email="user1@example.com",
                password="password1",
                alias="user1",
            ),
            User(
                id="user_2",
                email="user2@example.com",
                password="password2",
                alias="user2",
            ),
        ]

        self.repository.list_users.return_value = users

        # Act
        result = self.use_cases.list_users()

        # Assert
        expected_result = [user.to_dict_no_password() for user in users]
        assert result == expected_result
        self.repository.list_users.assert_called_once()

    def test_list_users_empty(self):
        """Test listing users when no users exist."""
        # Arrange
        self.repository.list_users.return_value = []

        # Act
        result = self.use_cases.list_users()

        # Assert
        assert result == []
        self.repository.list_users.assert_called_once()
