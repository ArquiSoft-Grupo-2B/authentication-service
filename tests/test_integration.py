"""
Integration tests that test the complete flow of the authentication service.
"""

import pytest
from src.application.user_use_cases import UserUseCases
from src.domain.services.user_service import UserService
from src.domain.entities.user import User
from src.infraestructure.repositories.in_memory_user_repository import (
    InMemoryUserRepository,
)


class TestAuthenticationServiceIntegration:
    """Integration tests for the authentication service components."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.repository = InMemoryUserRepository()
        self.service = UserService(self.repository)
        self.use_cases = UserUseCases(self.repository)

    def test_complete_user_lifecycle(self):
        """Test the complete lifecycle of a user through all layers."""
        # 1. Create user through use cases
        user = self.use_cases.create_user(
            email="test@example.com", password="password123", alias="testuser"
        )

        assert user.id == "1"
        assert user.email == "test@example.com"
        assert user.alias == "testuser"

        # 2. Verify user exists in repository
        repo_user = self.repository.get_user("1")
        assert repo_user is not None
        assert repo_user.email == "test@example.com"

        # 3. Verify user can be retrieved through service
        service_user = self.service.get_user("1")
        assert service_user is not None
        assert service_user.email == "test@example.com"

        # 4. Verify user can be retrieved through use cases
        use_case_user = self.use_cases.get_user("1")
        assert use_case_user is not None
        assert use_case_user.email == "test@example.com"

        # 5. Update user through use cases
        updated_data = {
            "id": "1",
            "email": "updated@example.com",
            "password": "newpassword123",
            "alias": "updateduser",
        }
        updated_user = self.use_cases.update_user(updated_data)
        assert updated_user.email == "updated@example.com"

        # 6. Verify update propagated to all layers
        repo_user = self.repository.get_user("1")
        assert repo_user.email == "updated@example.com"

        service_user = self.service.get_user("1")
        assert service_user.email == "updated@example.com"

        # 7. Delete user through use cases
        self.use_cases.delete_user("1")

        # 8. Verify deletion in all layers
        assert self.repository.get_user("1") is None
        assert self.service.get_user("1") is None
        assert self.use_cases.get_user("1") is None

    def test_business_rules_enforcement_across_layers(self):
        """Test that business rules are enforced across all layers."""
        # Test email uniqueness at service layer
        self.service.create_user("test@example.com", "password123", "user1")

        with pytest.raises(ValueError, match="User with this email already exists"):
            self.service.create_user("test@example.com", "password456", "user2")

        # Test email uniqueness at use case layer
        with pytest.raises(ValueError, match="User with this email already exists"):
            self.use_cases.create_user("test@example.com", "password789", "user3")

    def test_validation_across_layers(self):
        """Test that validation works across all layers."""
        # Create a user
        user = self.use_cases.create_user("test@example.com", "password123", "testuser")

        # Try to update with invalid data at service layer
        invalid_user = User(
            id="1", email="", password="password123", alias="testuser"  # Invalid email
        )

        with pytest.raises(ValueError, match="Invalid user data"):
            self.service.update_user(invalid_user)

        # Try to update with invalid data at use case layer
        invalid_user_data = {
            "id": "1",
            "email": "invalid-email",  # Invalid email format
            "password": "password123",
            "alias": "testuser",
        }

        with pytest.raises(ValueError, match="Invalid user data"):
            self.use_cases.update_user(invalid_user_data)

    def test_data_consistency_across_layers(self):
        """Test that data remains consistent across all layers."""
        # Create users through different layers
        repo_user = self.repository.create_user(
            "repo@example.com", "password123", "repouser"
        )
        service_user = self.service.create_user(
            "service@example.com", "password123", "serviceuser"
        )
        use_case_user = self.use_cases.create_user(
            "usecase@example.com", "password123", "usecaseuser"
        )

        # Verify all users exist and are accessible from all layers
        users_from_repo = list(self.repository.list_users())
        users_from_service = self.service.list_users()
        users_from_use_cases = self.use_cases.list_users()

        assert len(users_from_repo) == 3
        assert len(users_from_service) == 3
        assert len(users_from_use_cases) == 3

        # Verify specific user data consistency
        repo_retrieved = self.repository.get_user("1")
        service_retrieved = self.service.get_user("1")
        use_case_retrieved = self.use_cases.get_user("1")

        assert (
            repo_retrieved.email == service_retrieved.email == use_case_retrieved.email
        )
        assert (
            repo_retrieved.alias == service_retrieved.alias == use_case_retrieved.alias
        )

    def test_error_propagation_across_layers(self):
        """Test that errors are properly propagated across layers."""
        # Test repository errors propagate to service
        with pytest.raises(ValueError, match="User not found"):
            self.service.update_user(
                User(
                    id="999",
                    email="test@example.com",
                    password="password123",
                    alias="testuser",
                )
            )

        # Test repository errors propagate to use cases
        with pytest.raises(ValueError, match="User not found"):
            self.use_cases.delete_user("999")

        # Test service errors propagate to use cases
        self.use_cases.create_user("test@example.com", "password123", "user1")

        with pytest.raises(ValueError, match="User with this email already exists"):
            self.use_cases.create_user("test@example.com", "password456", "user2")

    def test_multiple_repositories_isolation(self):
        """Test that different repository instances remain isolated."""
        repo1 = InMemoryUserRepository()
        repo2 = InMemoryUserRepository()

        service1 = UserService(repo1)
        service2 = UserService(repo2)

        use_cases1 = UserUseCases(repo1)
        use_cases2 = UserUseCases(repo2)

        # Create users in different repositories
        user1 = use_cases1.create_user("user1@example.com", "password123", "user1")
        user2 = use_cases2.create_user("user2@example.com", "password123", "user2")

        # Verify isolation
        assert len(use_cases1.list_users()) == 1
        assert len(use_cases2.list_users()) == 1

        assert use_cases1.get_user("1") is not None
        assert use_cases1.get_user("2") is None

        assert use_cases2.get_user("1") is not None  # Different repository, same ID
        assert use_cases2.get_user("2") is None

    def test_complex_scenario_with_multiple_operations(self):
        """Test a complex scenario with multiple operations and validations."""
        # Create initial users
        users_data = [
            ("user1@example.com", "password123", "user1"),
            ("user2@example.com", "password456", "user2"),
            ("user3@example.com", "password789", "user3"),
        ]

        created_users = []
        for email, password, alias in users_data:
            user = self.use_cases.create_user(email, password, alias)
            created_users.append(user)

        # Verify all users exist
        all_users = self.use_cases.list_users()
        assert len(all_users) == 3

        # Try to create duplicate - should fail
        with pytest.raises(ValueError):
            self.use_cases.create_user("user1@example.com", "different", "different")

        # Update a user
        update_data = {
            "id": "2",
            "email": "updated_user2@example.com",
            "password": "newpassword456",
            "alias": "updated_user2",
        }
        updated_user = self.use_cases.update_user(update_data)
        assert updated_user.email == "updated_user2@example.com"

        # Try to update with existing email - should fail
        with pytest.raises(ValueError, match="Email already in use"):
            conflicting_update = {
                "id": "3",
                "email": "user1@example.com",  # Already exists
                "password": "password789",
                "alias": "user3",
            }
            self.use_cases.update_user(conflicting_update)

        # Delete a user
        self.use_cases.delete_user("1")

        # Verify final state
        final_users = self.use_cases.list_users()
        assert len(final_users) == 2

        # Verify specific users
        remaining_emails = [u["email"] for u in final_users]
        assert "user1@example.com" not in remaining_emails
        assert "updated_user2@example.com" in remaining_emails
        assert "user3@example.com" in remaining_emails

        # Verify no passwords in list
        for user_dict in final_users:
            assert "password" not in user_dict
