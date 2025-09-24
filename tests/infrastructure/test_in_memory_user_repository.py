import pytest
from src.infraestructure.repositories.in_memory_user_repository import (
    InMemoryUserRepository,
)
from src.domain.entities.user import User


class TestInMemoryUserRepository:
    """Test cases for InMemoryUserRepository."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.repository = InMemoryUserRepository()

    def test_create_user(self):
        """Test creating a user."""
        user = self.repository.create_user(
            "test@example.com", "password123", "testuser"
        )

        assert user.id == "1"
        assert user.email == "test@example.com"
        assert user.password == "password123"
        assert user.alias == "testuser"
        assert user in self.repository.users.values()

    def test_create_user_minimal_data(self):
        """Test creating a user with minimal data."""
        user = self.repository.create_user("test@example.com", "password123")

        assert user.id == "1"
        assert user.email == "test@example.com"
        assert user.password == "password123"
        assert user.alias is None

    def test_create_multiple_users_incremental_ids(self):
        """Test that multiple users get incremental IDs."""
        user1 = self.repository.create_user("test1@example.com", "password123")
        user2 = self.repository.create_user("test2@example.com", "password123")
        user3 = self.repository.create_user("test3@example.com", "password123")

        assert user1.id == "1"
        assert user2.id == "2"
        assert user3.id == "3"

    def test_get_user_existing(self):
        """Test getting an existing user by ID."""
        created_user = self.repository.create_user(
            "test@example.com", "password123", "testuser"
        )
        retrieved_user = self.repository.get_user("1")

        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.email == created_user.email
        assert retrieved_user.alias == created_user.alias

    def test_get_user_nonexistent(self):
        """Test getting a non-existent user returns None."""
        user = self.repository.get_user("999")
        assert user is None

    def test_get_user_by_email_existing(self):
        """Test getting an existing user by email."""
        created_user = self.repository.create_user(
            "test@example.com", "password123", "testuser"
        )
        retrieved_user = self.repository.get_user_by_email("test@example.com")

        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.email == created_user.email
        assert retrieved_user.alias == created_user.alias

    def test_get_user_by_email_nonexistent(self):
        """Test getting a non-existent user by email returns None."""
        user = self.repository.get_user_by_email("nonexistent@example.com")
        assert user is None

    def test_get_user_by_email_case_sensitive(self):
        """Test that email search is case sensitive."""
        self.repository.create_user("test@example.com", "password123")

        user_lower = self.repository.get_user_by_email("test@example.com")
        user_upper = self.repository.get_user_by_email("TEST@EXAMPLE.COM")

        assert user_lower is not None
        assert user_upper is None

    def test_update_user_existing(self):
        """Test updating an existing user."""
        # Create initial user
        original_user = self.repository.create_user(
            "test@example.com", "password123", "testuser"
        )

        # Update user data
        updated_user = User(
            id="1",
            email="updated@example.com",
            password="newpassword123",
            alias="updateduser",
            photo_url="http://example.com/photo.jpg",
        )

        result = self.repository.update_user(updated_user)

        assert result.id == "1"
        assert result.email == "updated@example.com"
        assert result.password == "newpassword123"
        assert result.alias == "updateduser"
        assert result.photo_url == "http://example.com/photo.jpg"

        # Verify the user is updated in storage
        retrieved_user = self.repository.get_user("1")
        assert retrieved_user.email == "updated@example.com"

    def test_update_user_nonexistent(self):
        """Test updating a non-existent user raises ValueError."""
        user = User(
            id="999", email="test@example.com", password="password123", alias="testuser"
        )

        with pytest.raises(ValueError, match="User not found"):
            self.repository.update_user(user)

    def test_delete_user_existing(self):
        """Test deleting an existing user."""
        # Create a user
        self.repository.create_user("test@example.com", "password123", "testuser")

        # Verify user exists
        assert self.repository.get_user("1") is not None

        # Delete the user
        self.repository.delete_user("1")

        # Verify user no longer exists
        assert self.repository.get_user("1") is None

    def test_delete_user_nonexistent(self):
        """Test deleting a non-existent user raises ValueError."""
        with pytest.raises(ValueError, match="User not found"):
            self.repository.delete_user("999")

    def test_list_users_empty(self):
        """Test listing users when repository is empty."""
        users = self.repository.list_users()
        assert list(users) == []

    def test_list_users_single(self):
        """Test listing users with single user."""
        created_user = self.repository.create_user(
            "test@example.com", "password123", "testuser"
        )
        users = list(self.repository.list_users())

        assert len(users) == 1
        assert users[0] == created_user

    def test_list_users_multiple(self):
        """Test listing users with multiple users."""
        user1 = self.repository.create_user("test1@example.com", "password123", "user1")
        user2 = self.repository.create_user("test2@example.com", "password123", "user2")
        user3 = self.repository.create_user("test3@example.com", "password123", "user3")

        users = list(self.repository.list_users())

        assert len(users) == 3
        assert user1 in users
        assert user2 in users
        assert user3 in users

    def test_list_users_after_deletion(self):
        """Test listing users after some users are deleted."""
        user1 = self.repository.create_user("test1@example.com", "password123", "user1")
        user2 = self.repository.create_user("test2@example.com", "password123", "user2")
        user3 = self.repository.create_user("test3@example.com", "password123", "user3")

        # Delete middle user
        self.repository.delete_user("2")

        users = list(self.repository.list_users())

        assert len(users) == 2
        assert user1 in users
        assert user2 not in users
        assert user3 in users

    def test_repository_isolation(self):
        """Test that different repository instances are isolated."""
        repo1 = InMemoryUserRepository()
        repo2 = InMemoryUserRepository()

        user1 = repo1.create_user("test1@example.com", "password123")
        user2 = repo2.create_user("test2@example.com", "password123")

        # Each repository should only have its own user
        assert len(list(repo1.list_users())) == 1
        assert len(list(repo2.list_users())) == 1
        assert repo1.get_user("1") is not None
        assert repo1.get_user("2") is None
        assert repo2.get_user("1") is not None
        assert repo2.get_user("2") is None
