"""
Configuration and fixtures for integration tests with Firebase.
"""

import pytest
import os
import uuid
from typing import List
from dotenv import load_dotenv
from src.infrastructure.repositories.firebase_user_repository import (
    FirebaseUserRepository,
)
from src.infrastructure.repositories.token_auth_repository import TokenAuthRepository
from src.domain.services.user_service import UserService
from src.domain.services.token_service import TokenService
from src.domain.entities.user import User

# Load environment variables for testing
load_dotenv(dotenv_path="configs/.env")


@pytest.fixture(scope="session")
def firebase_user_repository():
    """Create a Firebase user repository for integration tests."""
    return FirebaseUserRepository()


@pytest.fixture(scope="session")
def token_repository():
    """Create a token repository for integration tests."""
    return TokenAuthRepository()


@pytest.fixture(scope="session")
def user_service(firebase_user_repository):
    """Create a user service with Firebase repository."""
    return UserService(firebase_user_repository)


@pytest.fixture(scope="session")
def token_service(token_repository):
    """Create a token service with token repository."""
    return TokenService(token_repository)


@pytest.fixture(scope="session")
def test_users_cleanup():
    """
    Fixture to track test users and clean them up after tests.
    Returns a list to store user IDs that should be cleaned up.
    """
    created_users = []
    yield created_users

    # Cleanup after all tests in the session
    if created_users:
        repository = FirebaseUserRepository()
        for user_id in created_users:
            try:
                repository.delete_user(user_id)
                print(f"Cleaned up test user: {user_id}")
            except Exception as e:
                print(f"Failed to cleanup user {user_id}: {e}")


@pytest.fixture
def unique_test_email():
    """Generate a unique email for testing."""
    return f"test-{uuid.uuid4()}@integration-test.com"


@pytest.fixture
def test_user_data():
    """Standard test user data."""
    return {
        "email": f"test-{uuid.uuid4()}@integration-test.com",
        "password": "TestPassword123!",
        "alias": f"TestUser{uuid.uuid4().hex[:8]}",
    }


@pytest.fixture
def test_user_data_no_alias():
    """Test user data without alias."""
    return {
        "email": f"test-{uuid.uuid4()}@integration-test.com",
        "password": "TestPassword123!",
        "alias": None,
    }


@pytest.fixture
def invalid_test_user_data():
    """Invalid test user data for testing failures."""
    return [
        {"email": "invalid-email", "password": "TestPassword123!", "alias": "TestUser"},
        {
            "email": f"test-{uuid.uuid4()}@integration-test.com",
            "password": "123",  # Too short
            "alias": "TestUser",
        },
        {
            "email": "",  # Empty email
            "password": "TestPassword123!",
            "alias": "TestUser",
        },
    ]


@pytest.fixture
def skip_if_no_firebase_config():
    """Skip test if Firebase configuration is not available."""
    firebase_credentials = os.getenv("FIREBASE_CREDENTIALS_JSON")
    api_key = os.getenv("API_KEY")

    if not firebase_credentials or not api_key:
        pytest.skip("Firebase configuration not available for integration tests")
