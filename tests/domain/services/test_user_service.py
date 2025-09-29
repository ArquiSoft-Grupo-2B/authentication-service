import pytest
from src.domain.services.user_service import UserService
from src.domain.entities.user import User
from src.infraestructure.repositories.in_memory_user_repository import (
    InMemoryUserRepository,
)


class TestUserService:
    """Test cases for UserService."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.repository = InMemoryUserRepository()
        self.service = UserService(self.repository)

    def test_create_user_success(self):
        """Test successfully creating a new user."""
        user = self.service.create_user("test@example.com", "password123", "testuser")

        assert user.id == "1"
        assert user.email == "test@example.com"
        assert user.password == "password123"
        assert user.alias == "testuser"

    def test_create_user_minimal_data(self):
        """Test creating a user with minimal data."""
        user = self.service.create_user("test@example.com", "password123")

        assert user.id == "1"
        assert user.email == "test@example.com"
        assert user.password == "password123"
        assert user.alias is None

    def test_create_user_duplicate_email(self):
        """Test creating a user with duplicate email raises ValueError."""
        # Create first user
        self.service.create_user("test@example.com", "password123", "user1")

        # Attempt to create second user with same email
        with pytest.raises(ValueError, match="User with this email already exists"):
            self.service.create_user("test@example.com", "different_password", "user2")

    def test_get_user_existing(self):
        """Test getting an existing user by ID."""
        created_user = self.service.create_user(
            "test@example.com", "password123", "testuser"
        )
        retrieved_user = self.service.get_user("1")

        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.email == created_user.email

    def test_get_user_nonexistent(self):
        """Test getting a non-existent user returns None."""
        user = self.service.get_user("999")
        assert user is None

    def test_get_user_by_email_existing(self):
        """Test getting an existing user by email."""
        created_user = self.service.create_user(
            "test@example.com", "password123", "testuser"
        )
        retrieved_user = self.service.get_user_by_email("test@example.com")

        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.email == created_user.email

    def test_get_user_by_email_nonexistent(self):
        """Test getting a non-existent user by email returns None."""
        user = self.service.get_user_by_email("nonexistent@example.com")
        assert user is None

    def test_update_user_success(self):
        """Test successfully updating an existing user."""
        # Create initial user
        original_user = self.service.create_user(
            "test@example.com", "password123", "testuser"
        )

        # Update user data
        updated_user = User(
            id="1",
            email="updated@example.com",
            password="newpassword123",
            alias="updateduser",
        )

        result = self.service.update_user(updated_user)

        assert result.email == "updated@example.com"
        assert result.password == "newpassword123"
        assert result.alias == "updateduser"

    def test_update_user_invalid_data(self):
        """Test updating user with invalid data raises ValueError."""
        # Create initial user
        self.service.create_user("test@example.com", "password123", "testuser")

        # Create user with invalid data (empty email)
        invalid_user = User(id="1", email="", password="password123", alias="testuser")

        with pytest.raises(ValueError, match="Invalid user data"):
            self.service.update_user(invalid_user)

    def test_update_user_nonexistent(self):
        """Test updating a non-existent user raises ValueError."""
        user = User(
            id="999", email="test@example.com", password="password123", alias="testuser"
        )

        with pytest.raises(ValueError, match="User not found"):
            self.service.update_user(user)

    def test_update_user_email_already_in_use(self):
        """Test updating user email to one already in use raises ValueError."""
        # Create two users
        user1 = self.service.create_user("user1@example.com", "password123", "user1")
        user2 = self.service.create_user("user2@example.com", "password123", "user2")

        # Try to update user2's email to user1's email
        updated_user = User(
            id="2",
            email="user1@example.com",  # Email already in use
            password="password123",
            alias="user2",
        )

        with pytest.raises(ValueError, match="Email already in use"):
            self.service.update_user(updated_user)

    def test_update_user_same_email(self):
        """Test updating user with same email succeeds."""
        # Create user
        original_user = self.service.create_user(
            "test@example.com", "password123", "testuser"
        )

        # Update user with same email but different other data
        updated_user = User(
            id="1",
            email="test@example.com",  # Same email
            password="newpassword123",
            alias="newaliasuser",
        )

        result = self.service.update_user(updated_user)
        assert result.email == "test@example.com"
        assert result.alias == "newaliasuser"

    def test_delete_user_existing(self):
        """Test deleting an existing user."""
        # Create a user
        self.service.create_user("test@example.com", "password123", "testuser")

        # Verify user exists
        assert self.service.get_user("1") is not None

        # Delete the user
        self.service.delete_user("1")

        # Verify user no longer exists
        assert self.service.get_user("1") is None

    def test_delete_user_nonexistent(self):
        """Test deleting a non-existent user raises ValueError."""
        with pytest.raises(ValueError, match="User not found"):
            self.service.delete_user("999")

    def test_list_users_empty(self):
        """Test listing users when service has no users."""
        users = self.service.list_users()
        assert users == []

    def test_list_users_single(self):
        """Test listing users with single user."""
        created_user = self.service.create_user(
            "test@example.com", "password123", "testuser"
        )
        users = self.service.list_users()

        assert len(users) == 1
        assert users[0] == created_user

    def test_list_users_multiple(self):
        """Test listing users with multiple users."""
        user1 = self.service.create_user("test1@example.com", "password123", "user1")
        user2 = self.service.create_user("test2@example.com", "password123", "user2")
        user3 = self.service.create_user("test3@example.com", "password123", "user3")

        users = self.service.list_users()

        assert len(users) == 3
        assert user1 in users
        assert user2 in users
        assert user3 in users

    def test_list_users_after_operations(self):
        """Test listing users after various operations."""
        # Create users
        user1 = self.service.create_user("test1@example.com", "password123", "user1")
        user2 = self.service.create_user("test2@example.com", "password123", "user2")
        user3 = self.service.create_user("test3@example.com", "password123", "user3")

        # Delete one user
        self.service.delete_user("2")

        # Update another user
        updated_user = User(
            id="3",
            email="updated@example.com",
            password="newpassword",
            alias="updateduser",
        )
        self.service.update_user(updated_user)

        users = self.service.list_users()

        assert len(users) == 2
        assert user1 in users
        assert user2 not in users

        # Check that user3 was updated
        updated_user_in_list = next(u for u in users if u.id == "3")
        assert updated_user_in_list.email == "updated@example.com"
