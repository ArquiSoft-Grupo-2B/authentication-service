"""
Pytest configuration and shared fixtures for domain unit tests.
"""

import pytest
import sys
import os

# Add the src directory to Python path to enable imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {"email": "test@example.com", "password": "password123", "alias": "testuser"}


@pytest.fixture
def invalid_user_data():
    """Invalid user data for testing validation."""
    return [
        {"email": "", "password": "password123", "alias": "testuser"},  # Empty email
        {
            "email": "invalid-email",  # Invalid email format
            "password": "password123",
            "alias": "testuser",
        },
        {
            "email": "test@example.com",
            "password": "123",  # Short password
            "alias": "testuser",
        },
        {
            "email": "test@example.com",
            "password": "password123",
            "alias": "",  # Empty alias
        },
    ]
