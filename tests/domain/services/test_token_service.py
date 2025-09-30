import pytest
from unittest.mock import Mock
from src.domain.services.token_service import TokenService
from src.domain.entities.token import Token
from src.domain.entities.refresh_token import RefreshToken
from src.domain.repositories.token_repository import TokenRepository


class TestTokenService:
    """Test cases for TokenService."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.repository = Mock(spec=TokenRepository)
        self.service = TokenService(self.repository)

    def test_verify_token_valid(self):
        """Test verifying a valid token."""
        # Arrange
        expected_token = Token(
            local_id="123",
            email="test@example.com",
            alias="testuser",
            id_token="valid_token_123",
            registered=True,
            refresh_token="refresh_token_456",
            expires_in="3600",
        )
        self.repository.verify_token.return_value = expected_token

        # Act
        result = self.service.verify_token("valid_token_123")

        # Assert
        assert result == expected_token
        self.repository.verify_token.assert_called_once_with("valid_token_123")

    def test_verify_token_invalid(self):
        """Test verifying an invalid token returns None."""
        # Arrange
        self.repository.verify_token.return_value = None

        # Act
        result = self.service.verify_token("invalid_token")

        # Assert
        assert result is None
        self.repository.verify_token.assert_called_once_with("invalid_token")

    def test_verify_token_expired(self):
        """Test verifying an expired token returns None."""
        # Arrange
        self.repository.verify_token.return_value = None

        # Act
        result = self.service.verify_token("expired_token")

        # Assert
        assert result is None
        self.repository.verify_token.assert_called_once_with("expired_token")

    def test_refresh_token_success(self):
        """Test successfully refreshing a token."""
        # Arrange
        expected_refresh_token = RefreshToken(
            access_token="access_token_123",
            expires_in="3600",
            token_type="Bearer",
            refresh_token="new_refresh_token_456",
            id_token="id_token_789",
            user_id="user_123",
            project_id="project_456",
        )
        self.repository.refresh_token.return_value = expected_refresh_token

        # Act
        result = self.service.refresh_token("current_refresh_token")

        # Assert
        assert result == expected_refresh_token
        self.repository.refresh_token.assert_called_once_with("current_refresh_token")

    def test_refresh_token_invalid(self):
        """Test refreshing with an invalid token raises an exception."""
        # Arrange
        self.repository.refresh_token.side_effect = ValueError("Invalid refresh token")

        # Act & Assert
        with pytest.raises(ValueError, match="Invalid refresh token"):
            self.service.refresh_token("invalid_refresh_token")

        self.repository.refresh_token.assert_called_once_with("invalid_refresh_token")

    def test_refresh_token_expired(self):
        """Test refreshing with an expired token raises an exception."""
        # Arrange
        self.repository.refresh_token.side_effect = ValueError("Refresh token expired")

        # Act & Assert
        with pytest.raises(ValueError, match="Refresh token expired"):
            self.service.refresh_token("expired_refresh_token")

        self.repository.refresh_token.assert_called_once_with("expired_refresh_token")
