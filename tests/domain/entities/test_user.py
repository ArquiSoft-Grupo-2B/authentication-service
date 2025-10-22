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

    def test_validate_user_complete_valid(self):
        """Test validation with complete valid user data."""
        user = User(
            id="1", email="test@example.com", password="password123", alias="testuser"
        )

        assert user.validate_user_complete() is True

    def test_validate_user_login_valid(self):
        """Test validation with valid login data."""
        user = User(id="1", email="test@example.com", password="password123")

        assert user.validate_user_login() is True

    def test_validate_user_no_password_valid(self):
        """Test validation with valid data excluding password."""
        user = User(id="1", email="test@example.com", password="", alias="testuser")

        assert user.validate_user_no_password() is True

    def test_validate_invalid_email_empty(self):
        """Test validation fails with empty email."""
        user = User(id="1", email="", password="password123", alias="testuser")

        assert user.validate_user_complete() is False

    def test_validate_invalid_email_no_at(self):
        """Test validation fails with invalid email format (no @)."""
        user = User(
            id="1", email="testexample.com", password="password123", alias="testuser"
        )

        assert user.validate_user_complete() is False

    def test_validate_invalid_email_no_domain(self):
        """Test validation fails with invalid email format (no domain)."""
        user = User(id="1", email="test@", password="password123", alias="testuser")

        assert user.validate_user_complete() is False

    def test_validate_invalid_email_format(self):
        """Test validation fails with invalid email format."""
        user = User(
            id="1", email="not-an-email", password="password123", alias="testuser"
        )

        assert user.validate_user_complete() is False

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
            user = User(id="1", email=email, password="password123", alias="testuser")
            assert (
                user.validate_user_complete() is True
            ), f"Email {email} should be valid"

    def test_validate_short_password(self):
        """Test validation fails with password shorter than 8 characters."""
        user = User(
            id="1", email="test@example.com", password="1234567", alias="testuser"
        )

        assert user.validate_user_complete() is False

    def test_validate_empty_password(self):
        """Test validation fails with empty password."""
        user = User(id="1", email="test@example.com", password="", alias="testuser")

        assert user.validate_user_complete() is False

    def test_validate_none_password(self):
        """Test validation fails with None password."""
        user = User(id="1", email="test@example.com", password=None, alias="testuser")

        assert user.validate_user_complete() is False

    def test_validate_empty_alias(self):
        """Test validation fails with empty alias."""
        user = User(id="1", email="test@example.com", password="password123", alias="")

        assert user.validate_user_complete() is False

    def test_validate_whitespace_only_alias(self):
        """Test validation fails with whitespace-only alias."""
        user = User(
            id="1", email="test@example.com", password="password123", alias="   "
        )

        assert user.validate_user_complete() is False

    def test_validate_none_alias(self):
        """Test validation fails with None alias for complete validation."""
        user = User(
            id="1", email="test@example.com", password="password123", alias=None
        )

        assert user.validate_user_complete() is False
        assert user.validate_user_login() is True  # Login doesn't require alias

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

    def test_validate_email_static_method(self):
        """Test the static email validation method directly."""
        # Valid emails
        assert User.validate_email("test@example.com") is True
        assert User.validate_email("user.name@domain.co.uk") is True
        assert User.validate_email("user+tag@example.com") is True

        # Invalid emails
        assert User.validate_email("invalid") is False
        assert User.validate_email("@example.com") is False
        assert User.validate_email("test@") is False
        assert User.validate_email("") is False

    def test_validate_password_static_method(self):
        """Test the static password validation method directly."""
        # Valid passwords
        assert User.validate_password("password123") is True
        assert User.validate_password("12345678") is True
        assert User.validate_password("very_long_password") is True

        # Invalid passwords
        assert User.validate_password("1234567") is False  # Too short
        assert User.validate_password("") is False  # Empty
        assert User.validate_password(None) is False  # None

    def test_validate_alias_static_method(self):
        """Test the static alias validation method directly."""
        # Valid aliases
        assert User.validate_alias("abc") is True  # Minimum length
        assert User.validate_alias("testuser") is True
        assert User.validate_alias("a" * 30) is True  # Maximum length

        # Invalid aliases
        assert User.validate_alias("ab") is False  # Too short
        assert User.validate_alias("a" * 31) is False  # Too long
        assert User.validate_alias("") is False  # Empty
        assert User.validate_alias(None) is False  # None

    def test_validate_user_login_scenarios(self):
        """Test various login validation scenarios."""
        # Valid login
        user = User(id="1", email="test@example.com", password="password123")
        assert user.validate_user_login() is True

        # Invalid email
        user = User(id="1", email="invalid-email", password="password123")
        assert user.validate_user_login() is False

        # Invalid password
        user = User(id="1", email="test@example.com", password="short")
        assert user.validate_user_login() is False

        # Both invalid
        user = User(id="1", email="invalid", password="short")
        assert user.validate_user_login() is False

    def test_validate_user_no_password_scenarios(self):
        """Test validation excluding password scenarios."""
        # Valid data without password
        user = User(id="1", email="test@example.com", password="", alias="testuser")
        assert user.validate_user_no_password() is True

        # Invalid email
        user = User(id="1", email="invalid", password="", alias="testuser")
        assert user.validate_user_no_password() is False

        # Invalid alias
        user = User(id="1", email="test@example.com", password="", alias="ab")
        assert user.validate_user_no_password() is False

        # No alias (should fail for complete validation)
        user = User(id="1", email="test@example.com", password="", alias=None)
        assert user.validate_user_no_password() is False
