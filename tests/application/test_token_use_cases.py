import pytest
from unittest.mock import Mock
from src.application.token_use_cases import TokenUseCases
from src.domain.entities.token import Token
from src.domain.entities.refresh_token import RefreshToken
from src.domain.repositories.token_repository import TokenRepository


class TestTokenUseCases:
    """Test cases for TokenUseCases."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.repository = Mock(spec=TokenRepository)
        self.use_cases = TokenUseCases(self.repository)

    def test_verify_token_valid(self):
        """Test verifying a valid token."""
        # Arrange
        id_token = "valid_token_123"
        expected_token = Token(
            local_id="123",
            email="test@example.com",
            alias="testuser",
            id_token=id_token,
            registered=True,
            refresh_token="refresh_token_456",
            expires_in="3600",
        )
        self.repository.verify_token.return_value = expected_token

        # Act
        result = self.use_cases.verify_token(id_token)

        # Assert
        assert result == expected_token.to_dict()
        self.repository.verify_token.assert_called_once_with(id_token)

    def test_verify_token_invalid(self):
        """Test verifying an invalid token."""
        # Arrange
        id_token = "invalid_token"
        self.repository.verify_token.return_value = None

        # Act
        result = self.use_cases.verify_token(id_token)

        # Assert
        assert result is None
        self.repository.verify_token.assert_called_once_with(id_token)

    def test_refresh_token_valid(self):
        """Test refreshing a valid token."""
        # Arrange
        refresh_token_str = "valid_refresh_token"
        expected_refresh_token = RefreshToken(
            access_token="new_access_token",
            expires_in="3600",
            token_type="refresh_token",
            refresh_token="new_refresh_token",
            id_token="new_id_token",
            user_id="123",
            project_id="project_123",
        )
        self.repository.refresh_token.return_value = expected_refresh_token

        # Act
        result = self.use_cases.refresh_token(refresh_token_str)

        # Assert
        assert result == expected_refresh_token
        self.repository.refresh_token.assert_called_once_with(refresh_token_str)

    def test_refresh_token_invalid(self):
        """Test refreshing an invalid token."""
        # Arrange
        refresh_token_str = "invalid_refresh_token"
        self.repository.refresh_token.return_value = None

        # Act
        result = self.use_cases.refresh_token(refresh_token_str)

        # Assert
        assert result is None
        self.repository.refresh_token.assert_called_once_with(refresh_token_str)
