import pytest
from src.domain.entities.token import Token


class TestToken:
    """Test cases for Token entity."""

    def test_token_creation(self):
        """Test creating a token with valid data."""
        token = Token(
            local_id="123",
            email="test@example.com",
            alias="testuser",
            id_token="id_token_123",
            registered=True,
            refresh_token="refresh_token_456",
            expires_in="3600",
        )

        assert token.local_id == "123"
        assert token.email == "test@example.com"
        assert token.alias == "testuser"
        assert token.id_token == "id_token_123"
        assert token.registered is True
        assert token.refresh_token == "refresh_token_456"
        assert token.expires_in == "3600"

    def test_token_to_dict(self):
        """Test converting token to dictionary."""
        token = Token(
            local_id="123",
            email="test@example.com",
            alias="testuser",
            id_token="id_token_123",
            registered=True,
            refresh_token="refresh_token_456",
            expires_in="3600",
        )

        result = token.to_dict()
        expected = {
            "local_id": "123",
            "email": "test@example.com",
            "alias": "testuser",
            "id_token": "id_token_123",
            "registered": True,
            "refresh_token": "refresh_token_456",
            "expires_in": "3600",
        }

        assert result == expected

    def test_token_with_unregistered_user(self):
        """Test creating a token for an unregistered user."""
        token = Token(
            local_id="456",
            email="newuser@example.com",
            alias="newuser",
            id_token="id_token_456",
            registered=False,
            refresh_token="refresh_token_789",
            expires_in="1800",
        )

        assert token.registered is False
        result = token.to_dict()
        assert result["registered"] is False
