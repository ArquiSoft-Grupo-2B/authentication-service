import pytest
from src.domain.entities.refresh_token import RefreshToken


class TestRefreshToken:
    """Test cases for RefreshToken entity."""

    def test_refresh_token_creation(self):
        """Test creating a refresh token with valid data."""
        refresh_token = RefreshToken(
            access_token="access_token_123",
            expires_in="3600",
            token_type="Bearer",
            refresh_token="refresh_token_456",
            id_token="id_token_789",
            user_id="user_123",
            project_id="project_456",
        )

        assert refresh_token.access_token == "access_token_123"
        assert refresh_token.expires_in == "3600"
        assert refresh_token.token_type == "Bearer"
        assert refresh_token.refresh_token == "refresh_token_456"
        assert refresh_token.id_token == "id_token_789"
        assert refresh_token.user_id == "user_123"
        assert refresh_token.project_id == "project_456"

    def test_refresh_token_different_token_type(self):
        """Test creating a refresh token with different token type."""
        refresh_token = RefreshToken(
            access_token="access_token_abc",
            expires_in="1800",
            token_type="JWT",
            refresh_token="refresh_token_def",
            id_token="id_token_ghi",
            user_id="user_456",
            project_id="project_789",
        )

        assert refresh_token.token_type == "JWT"
        assert refresh_token.expires_in == "1800"

    def test_refresh_token_equality(self):
        """Test that two refresh tokens with same data are equal."""
        refresh_token1 = RefreshToken(
            access_token="token123",
            expires_in="3600",
            token_type="Bearer",
            refresh_token="refresh123",
            id_token="id123",
            user_id="user123",
            project_id="project123",
        )

        refresh_token2 = RefreshToken(
            access_token="token123",
            expires_in="3600",
            token_type="Bearer",
            refresh_token="refresh123",
            id_token="id123",
            user_id="user123",
            project_id="project123",
        )

        assert refresh_token1 == refresh_token2
