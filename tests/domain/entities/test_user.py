import pytest
from src.domain.entities.user import User


class TestUser:
    """Test cases for User entity."""

    def test_user_creation(self):
        """Test creating a user with valid data."""
        user = User(
            id="1", email="test@example.com", password="password123", alias="testuser"
        )

        assert user.id == "1"
        assert user.email == "test@example.com"
        assert user.password == "password123"
        assert user.alias == "testuser"
        assert user.photo_url is None

    def test_user_creation_minimal_data(self):
        """Test creating a user with minimal required data."""
        user = User(id="1", email="test@example.com", password="password123")

        assert user.id == "1"
        assert user.email == "test@example.com"
        assert user.password == "password123"
        assert user.alias is None
        assert user.photo_url is None

    def test_validate_valid_user(self):
        """Test validation with valid user data."""
        user = User(
            id="1", email="test@example.com", password="password123", alias="testuser"
        )

        assert user.validate() is True

    def test_validate_invalid_email_empty(self):
        """Test validation fails with empty email."""
        user = User(id="1", email="", password="password123")

        assert user.validate() is False

    def test_validate_invalid_email_no_at(self):
        """Test validation fails with invalid email format (no @)."""
        user = User(id="1", email="testexample.com", password="password123")

        assert user.validate() is False

    def test_validate_invalid_email_no_domain(self):
        """Test validation fails with invalid email format (no domain)."""
        user = User(id="1", email="test@", password="password123")

        assert user.validate() is False

    def test_validate_invalid_email_format(self):
        """Test validation fails with invalid email format."""
        user = User(id="1", email="not-an-email", password="password123")

        assert user.validate() is False

    def test_validate_valid_email_formats(self):
        """Test validation with various valid email formats."""
        valid_emails = [
            "test@example.com",
            "user.name@example.com",
            "user+tag@example.com",
            "user123@example123.co.uk",
            "test_user@example-site.org",
        ]

        for email in valid_emails:
            user = User(id="1", email=email, password="password123")
            assert user.validate() is True, f"Email {email} should be valid"

    def test_validate_short_password(self):
        """Test validation fails with password shorter than 8 characters."""
        user = User(id="1", email="test@example.com", password="1234567")

        assert user.validate() is False

    def test_validate_empty_password(self):
        """Test validation fails with empty password."""
        user = User(id="1", email="test@example.com", password="")

        assert user.validate() is False

    def test_validate_none_password(self):
        """Test validation fails with None password."""
        user = User(id="1", email="test@example.com", password=None)

        assert user.validate() is False

    def test_validate_empty_alias(self):
        """Test validation fails with empty alias."""
        user = User(id="1", email="test@example.com", password="password123", alias="")

        assert user.validate() is False

    def test_validate_whitespace_only_alias(self):
        """Test validation fails with whitespace-only alias."""
        user = User(
            id="1", email="test@example.com", password="password123", alias="   "
        )

        assert user.validate() is False

    def test_validate_none_alias(self):
        """Test validation passes with None alias."""
        user = User(
            id="1", email="test@example.com", password="password123", alias=None
        )

        assert user.validate() is True

    def test_to_dict_no_password(self):
        """Test converting user to dictionary without password."""
        user = User(
            id="1",
            email="test@example.com",
            password="password123",
            alias="testuser",
            photo_url="http://example.com/photo.jpg",
        )

        result = user.to_dict_no_password()
        expected = {
            "id": "1",
            "email": "test@example.com",
            "alias": "testuser",
            "photo_url": "http://example.com/photo.jpg",
        }

        assert result == expected
        assert "password" not in result

    def test_to_dict_no_password_minimal(self):
        """Test converting user with minimal data to dictionary without password."""
        user = User(id="1", email="test@example.com", password="password123")

        result = user.to_dict_no_password()
        expected = {
            "id": "1",
            "email": "test@example.com",
            "alias": None,
            "photo_url": None,
        }

        assert result == expected
        assert "password" not in result

    def test_is_valid_email_private_method(self):
        """Test the private email validation method directly."""
        user = User(id="1", email="test@example.com", password="password123")

        # Valid emails
        assert user._is_valid_email("test@example.com") is True
        assert user._is_valid_email("user.name@domain.co.uk") is True

        # Invalid emails
        assert user._is_valid_email("invalid") is False
        assert user._is_valid_email("@example.com") is False
        assert user._is_valid_email("test@") is False
        assert user._is_valid_email("") is False
