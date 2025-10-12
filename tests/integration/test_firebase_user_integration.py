"""
Integration tests for Firebase User Repository and User Service.
These tests interact with actual Firebase services.
"""

import pytest
import time
from src.domain.entities.user import User
from src.domain.services.user_service import UserService
from src.infrastructure.repositories.firebase_user_repository import (
    FirebaseUserRepository,
)


@pytest.mark.integration
class TestFirebaseUserIntegration:
    """Integration tests for user management with Firebase."""

    def test_create_user_success(
        self,
        user_service,
        test_user_data,
        test_users_cleanup,
        skip_if_no_firebase_config,
    ):
        """Test creating a user successfully in Firebase."""
        # Act
        created_user = user_service.create_user(
            email=test_user_data["email"],
            password=test_user_data["password"],
            alias=test_user_data["alias"],
        )

        # Add to cleanup list
        test_users_cleanup.append(created_user.id)

        # Assert
        assert created_user is not None
        assert created_user.id is not None
        assert created_user.email == test_user_data["email"]
        assert created_user.alias == test_user_data["alias"]
        assert created_user.password == ""  # Password should not be returned

    def test_create_user_without_alias(
        self,
        user_service,
        test_user_data_no_alias,
        test_users_cleanup,
        skip_if_no_firebase_config,
    ):
        """Test creating a user without alias."""
        # Act
        created_user = user_service.create_user(
            email=test_user_data_no_alias["email"],
            password=test_user_data_no_alias["password"],
            alias=test_user_data_no_alias["alias"],
        )

        # Add to cleanup list
        test_users_cleanup.append(created_user.id)

        # Assert
        assert created_user is not None
        assert created_user.id is not None
        assert created_user.email == test_user_data_no_alias["email"]
        assert created_user.alias is None

    def test_create_user_duplicate_email_fails(
        self,
        user_service,
        test_user_data,
        test_users_cleanup,
        skip_if_no_firebase_config,
    ):
        """Test that creating a user with duplicate email fails."""
        # Arrange - Create first user
        created_user = user_service.create_user(
            email=test_user_data["email"],
            password=test_user_data["password"],
            alias=test_user_data["alias"],
        )
        test_users_cleanup.append(created_user.id)

        # Act & Assert - Try to create user with same email
        with pytest.raises(ValueError, match="User with this email already exists"):
            user_service.create_user(
                email=test_user_data["email"],
                password="DifferentPassword123!",
                alias="DifferentAlias",
            )

    def test_create_user_invalid_data_fails(
        self, user_service, invalid_test_user_data, skip_if_no_firebase_config
    ):
        """Test that creating users with invalid data fails."""
        for invalid_data in invalid_test_user_data:
            with pytest.raises(Exception):  # Could be ValueError or Firebase exception
                user_service.create_user(
                    email=invalid_data["email"],
                    password=invalid_data["password"],
                    alias=invalid_data["alias"],
                )

    def test_get_user_by_id_success(
        self,
        user_service,
        test_user_data,
        test_users_cleanup,
        skip_if_no_firebase_config,
    ):
        """Test getting a user by ID successfully."""
        # Arrange - Create a user first
        created_user = user_service.create_user(
            email=test_user_data["email"],
            password=test_user_data["password"],
            alias=test_user_data["alias"],
        )
        test_users_cleanup.append(created_user.id)

        # Act
        retrieved_user = user_service.get_user(created_user.id)

        # Assert
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.email == created_user.email
        assert retrieved_user.alias == created_user.alias

    def test_get_user_by_id_not_found(self, user_service, skip_if_no_firebase_config):
        """Test getting a non-existent user by ID."""
        # Act & Assert
        with pytest.raises(ValueError, match="User not found"):
            user_service.get_user("non-existent-user-id")

    def test_get_user_by_email_success(
        self,
        user_service,
        test_user_data,
        test_users_cleanup,
        skip_if_no_firebase_config,
    ):
        """Test getting a user by email successfully."""
        # Arrange - Create a user first
        created_user = user_service.create_user(
            email=test_user_data["email"],
            password=test_user_data["password"],
            alias=test_user_data["alias"],
        )
        test_users_cleanup.append(created_user.id)

        # Act
        retrieved_user = user_service.get_user_by_email(test_user_data["email"])

        # Assert
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.email == created_user.email
        assert retrieved_user.alias == created_user.alias

    def test_get_user_by_email_not_found(
        self, user_service, skip_if_no_firebase_config
    ):
        """Test getting a non-existent user by email returns None."""
        # Act
        result = user_service.get_user_by_email("nonexistent@example.com")

        # Assert
        assert result is None

    def test_list_users(
        self,
        user_service,
        test_user_data,
        test_users_cleanup,
        skip_if_no_firebase_config,
    ):
        """Test listing all users includes our test user."""
        # Arrange - Get initial count
        initial_users = user_service.list_users()
        initial_count = len(initial_users)

        # Create a test user
        created_user = user_service.create_user(
            email=test_user_data["email"],
            password=test_user_data["password"],
            alias=test_user_data["alias"],
        )
        test_users_cleanup.append(created_user.id)

        # Act
        users_after_creation = user_service.list_users()

        # Assert
        assert len(users_after_creation) == initial_count + 1

        # Find our created user in the list
        created_user_in_list = next(
            (user for user in users_after_creation if user.id == created_user.id), None
        )
        assert created_user_in_list is not None
        assert created_user_in_list.email == test_user_data["email"]

    def test_update_user_success(
        self,
        user_service,
        test_user_data,
        test_users_cleanup,
        skip_if_no_firebase_config,
    ):
        """Test updating a user successfully."""
        # Arrange - Create a user first
        created_user = user_service.create_user(
            email=test_user_data["email"],
            password=test_user_data["password"],
            alias=test_user_data["alias"],
        )
        test_users_cleanup.append(created_user.id)

        # Modify user data
        updated_user = User(
            id=created_user.id,
            email=created_user.email,  # Keep same email to avoid conflicts
            password="NewPassword123!",
            alias="UpdatedAlias",
        )

        # Act
        result = user_service.update_user(updated_user)

        # Assert
        assert result is not None
        assert result.id == created_user.id
        assert result.email == created_user.email
        assert result.alias == "UpdatedAlias"

        # Verify the update persisted
        retrieved_user = user_service.get_user(created_user.id)
        assert retrieved_user.alias == "UpdatedAlias"

    def test_update_user_not_found(self, user_service, skip_if_no_firebase_config):
        """Test updating a non-existent user fails."""
        # Arrange
        non_existent_user = User(
            id="non-existent-id",
            email="test@example.com",
            password="password123",
            alias="alias",
        )

        # Act & Assert
        with pytest.raises(ValueError, match="User not found"):
            user_service.update_user(non_existent_user)

    def test_update_user_email_conflict(
        self,
        user_service,
        test_user_data,
        test_users_cleanup,
        skip_if_no_firebase_config,
    ):
        """Test updating user with email that belongs to another user fails."""
        # Arrange - Create two users
        user1_data = test_user_data.copy()
        user1 = user_service.create_user(
            email=user1_data["email"],
            password=user1_data["password"],
            alias=user1_data["alias"],
        )
        test_users_cleanup.append(user1.id)

        user2_data = {
            "email": f"second-{user1_data['email']}",
            "password": "Password123!",
            "alias": "SecondUser",
        }
        user2 = user_service.create_user(
            email=user2_data["email"],
            password=user2_data["password"],
            alias=user2_data["alias"],
        )
        test_users_cleanup.append(user2.id)

        # Try to update user2 with user1's email
        user2_with_conflicting_email = User(
            id=user2.id,
            email=user1.email,  # This should cause conflict
            password="NewPassword123!",
            alias="UpdatedUser2",
        )

        # Act & Assert
        with pytest.raises(ValueError, match="Email already in use"):
            user_service.update_user(user2_with_conflicting_email)

    def test_send_password_reset_email_success(
        self,
        user_service,
        test_user_data,
        test_users_cleanup,
        skip_if_no_firebase_config,
    ):
        """Test sending password reset email for existing user."""
        # Arrange - Create a user first
        created_user = user_service.create_user(
            email=test_user_data["email"],
            password=test_user_data["password"],
            alias=test_user_data["alias"],
        )
        test_users_cleanup.append(created_user.id)

        # Act
        result = user_service.send_password_reset_email(test_user_data["email"])

        # Assert
        assert result is not None
        assert result.get("success") is True

    def test_send_password_reset_email_user_not_found(
        self, user_service, skip_if_no_firebase_config
    ):
        """Test sending password reset email for non-existent user fails."""
        # Act & Assert
        with pytest.raises(ValueError, match="No user found with this email"):
            user_service.send_password_reset_email("nonexistent@example.com")

    def test_send_password_reset_email_invalid_format(
        self, user_service, skip_if_no_firebase_config
    ):
        """Test sending password reset email with invalid email format fails."""
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid email format"):
            user_service.send_password_reset_email("invalid-email-format")

    def test_delete_user_success(
        self, user_service, test_user_data, skip_if_no_firebase_config
    ):
        """Test deleting a user successfully."""
        # Arrange - Create a user first
        created_user = user_service.create_user(
            email=test_user_data["email"],
            password=test_user_data["password"],
            alias=test_user_data["alias"],
        )

        # Act
        user_service.delete_user(created_user.id)

        # Assert - User should no longer exist
        with pytest.raises(ValueError, match="User not found"):
            user_service.get_user(created_user.id)

    def test_delete_user_not_found(self, user_service, skip_if_no_firebase_config):
        """Test deleting a non-existent user fails."""
        # Act & Assert
        with pytest.raises(ValueError, match="User not found"):
            user_service.delete_user("non-existent-user-id")

    def test_full_user_lifecycle(
        self, user_service, test_user_data, skip_if_no_firebase_config
    ):
        """Test complete user lifecycle: create, read, update, delete."""
        created_user = None
        try:
            # Create
            created_user = user_service.create_user(
                email=test_user_data["email"],
                password=test_user_data["password"],
                alias=test_user_data["alias"],
            )
            assert created_user is not None

            # Read
            retrieved_user = user_service.get_user(created_user.id)
            assert retrieved_user.email == test_user_data["email"]

            # Update
            updated_user = User(
                id=created_user.id,
                email=created_user.email,
                password="NewPassword123!",
                alias="UpdatedAlias",
            )
            result = user_service.update_user(updated_user)
            assert result.alias == "UpdatedAlias"

            # Delete
            user_service.delete_user(created_user.id)

            # Verify deletion
            with pytest.raises(ValueError, match="User not found"):
                user_service.get_user(created_user.id)

        except Exception as e:
            # Cleanup in case of test failure
            if created_user and created_user.id:
                try:
                    user_service.delete_user(created_user.id)
                except:
                    pass
            raise e
