import pytest
from src.application.user_use_cases import UserUseCases
from src.domain.entities.user import User
from src.infraestructure.repositories.in_memory_user_repository import (
    InMemoryUserRepository,
)


class TestUserUseCases:
    """Test cases for UserUseCases."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.repository = InMemoryUserRepository()
        self.use_cases = UserUseCases(self.repository)

    def test_create_user_success(self):
        """Test successfully creating a new user."""
        user = self.use_cases.create_user("test@example.com", "password123", "testuser")

        assert isinstance(user, User)
        assert user.id == "1"
        assert user.email == "test@example.com"
        assert user.password == "password123"
        assert user.alias == "testuser"

    def test_create_user_minimal_data(self):
        """Test creating a user with minimal data."""
        user = self.use_cases.create_user("test@example.com", "password123")

        assert isinstance(user, User)
        assert user.id == "1"
        assert user.email == "test@example.com"
        assert user.password == "password123"
        assert user.alias is None

    def test_create_user_duplicate_email(self):
        """Test creating a user with duplicate email raises ValueError."""
        # Create first user
        self.use_cases.create_user("test@example.com", "password123", "user1")

        # Attempt to create second user with same email
        with pytest.raises(ValueError, match="User with this email already exists"):
            self.use_cases.create_user(
                "test@example.com", "different_password", "user2"
            )

    def test_get_user_existing(self):
        """Test getting an existing user by ID."""
        created_user = self.use_cases.create_user(
            "test@example.com", "password123", "testuser"
        )
        retrieved_user = self.use_cases.get_user("1")

        assert retrieved_user is not None
        assert isinstance(retrieved_user, User)
        assert retrieved_user.id == created_user.id
        assert retrieved_user.email == created_user.email

    def test_get_user_nonexistent(self):
        """Test getting a non-existent user returns None."""
        user = self.use_cases.get_user("999")
        assert user is None

    def test_update_user_success(self):
        """Test successfully updating an existing user."""
        # Create initial user
        original_user = self.use_cases.create_user(
            "test@example.com", "password123", "testuser"
        )

        # Prepare updated user data
        updated_user_data = {
            "id": "1",
            "email": "updated@example.com",
            "password": "newpassword123",
            "alias": "updateduser",
        }

        result = self.use_cases.update_user(updated_user_data)

        assert isinstance(result, User)
        assert result.email == "updated@example.com"
        assert result.password == "newpassword123"
        assert result.alias == "updateduser"

    def test_update_user_invalid_data(self):
        """Test updating user with invalid data raises ValueError."""
        # Create initial user
        self.use_cases.create_user("test@example.com", "password123", "testuser")

        # Prepare invalid user data (empty email)
        invalid_user_data = {
            "id": "1",
            "email": "",
            "password": "password123",
            "alias": "testuser",
        }

        with pytest.raises(ValueError, match="Invalid user data"):
            self.use_cases.update_user(invalid_user_data)

    def test_update_user_nonexistent(self):
        """Test updating a non-existent user raises ValueError."""
        user_data = {
            "id": "999",
            "email": "test@example.com",
            "password": "password123",
            "alias": "testuser",
        }

        with pytest.raises(ValueError, match="User not found"):
            self.use_cases.update_user(user_data)

    def test_update_user_email_already_in_use(self):
        """Test updating user email to one already in use raises ValueError."""
        # Create two users
        user1 = self.use_cases.create_user("user1@example.com", "password123", "user1")
        user2 = self.use_cases.create_user("user2@example.com", "password123", "user2")

        # Try to update user2's email to user1's email
        updated_user_data = {
            "id": "2",
            "email": "user1@example.com",  # Email already in use
            "password": "password123",
            "alias": "user2",
        }

        with pytest.raises(ValueError, match="Email already in use"):
            self.use_cases.update_user(updated_user_data)

    def test_delete_user_existing(self):
        """Test deleting an existing user."""
        # Create a user
        self.use_cases.create_user("test@example.com", "password123", "testuser")

        # Verify user exists
        assert self.use_cases.get_user("1") is not None

        # Delete the user
        self.use_cases.delete_user("1")

        # Verify user no longer exists
        assert self.use_cases.get_user("1") is None

    def test_delete_user_nonexistent(self):
        """Test deleting a non-existent user raises ValueError."""
        with pytest.raises(ValueError, match="User not found"):
            self.use_cases.delete_user("999")

    def test_list_users_empty(self):
        """Test listing users when no users exist."""
        users = self.use_cases.list_users()
        assert users == []

    def test_list_users_single(self):
        """Test listing users with single user."""
        created_user = self.use_cases.create_user(
            "test@example.com", "password123", "testuser"
        )
        users = self.use_cases.list_users()

        assert len(users) == 1
        assert isinstance(users[0], dict)
        assert users[0]["id"] == "1"
        assert users[0]["email"] == "test@example.com"
        assert users[0]["alias"] == "testuser"
        assert "password" not in users[0]  # Password should be excluded

    def test_list_users_multiple(self):
        """Test listing users with multiple users."""
        user1 = self.use_cases.create_user("test1@example.com", "password123", "user1")
        user2 = self.use_cases.create_user("test2@example.com", "password123", "user2")
        user3 = self.use_cases.create_user("test3@example.com", "password123", "user3")

        users = self.use_cases.list_users()

        assert len(users) == 3

        # Verify all users are returned as dictionaries without passwords
        user_ids = [u["id"] for u in users]
        user_emails = [u["email"] for u in users]

        assert "1" in user_ids
        assert "2" in user_ids
        assert "3" in user_ids

        assert "test1@example.com" in user_emails
        assert "test2@example.com" in user_emails
        assert "test3@example.com" in user_emails

        # Verify no passwords are included
        for user_dict in users:
            assert "password" not in user_dict

    def test_list_users_after_deletion(self):
        """Test listing users after some users are deleted."""
        user1 = self.use_cases.create_user("test1@example.com", "password123", "user1")
        user2 = self.use_cases.create_user("test2@example.com", "password123", "user2")
        user3 = self.use_cases.create_user("test3@example.com", "password123", "user3")

        # Delete middle user
        self.use_cases.delete_user("2")

        users = self.use_cases.list_users()

        assert len(users) == 2
        user_ids = [u["id"] for u in users]
        assert "1" in user_ids
        assert "2" not in user_ids
        assert "3" in user_ids

    def test_list_users_after_update(self):
        """Test listing users after updating one."""
        user1 = self.use_cases.create_user("test1@example.com", "password123", "user1")
        user2 = self.use_cases.create_user("test2@example.com", "password123", "user2")

        # Update user2
        updated_user_data = {
            "id": "2",
            "email": "updated@example.com",
            "password": "newpassword123",
            "alias": "updateduser",
        }
        self.use_cases.update_user(updated_user_data)

        users = self.use_cases.list_users()

        assert len(users) == 2

        # Find the updated user in the list
        updated_user_in_list = next(u for u in users if u["id"] == "2")
        assert updated_user_in_list["email"] == "updated@example.com"
        assert updated_user_in_list["alias"] == "updateduser"
        assert "password" not in updated_user_in_list

    def test_integration_full_workflow(self):
        """Test a complete workflow with all operations."""
        # Create users
        user1 = self.use_cases.create_user("user1@example.com", "password123", "user1")
        user2 = self.use_cases.create_user("user2@example.com", "password456", "user2")

        # List users
        users = self.use_cases.list_users()
        assert len(users) == 2

        # Get specific user
        retrieved_user = self.use_cases.get_user("1")
        assert retrieved_user.email == "user1@example.com"

        # Update user
        updated_data = {
            "id": "1",
            "email": "updated_user1@example.com",
            "password": "newpassword123",
            "alias": "updated_user1",
        }
        updated_user = self.use_cases.update_user(updated_data)
        assert updated_user.email == "updated_user1@example.com"

        # Delete user
        self.use_cases.delete_user("2")

        # Final list should have one user
        final_users = self.use_cases.list_users()
        assert len(final_users) == 1
        assert final_users[0]["email"] == "updated_user1@example.com"
