from dataclasses import dataclass
from typing import Optional
import re


@dataclass
class User:
    """
    Represents a user and business rules in the system.
    """

    id: str
    email: str
    password: str
    alias: str | None = None
    photo_url: str | None = None

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", "")
        self.email = kwargs.get("email", "")
        self.password = kwargs.get("password", "")
        self.alias = kwargs.get("alias")
        self.photo_url = kwargs.get("photo_url")

    def validate_user_complete(self) -> bool:
        """Validate user data according to business rules."""
        if not self.validate_email(self.email):
            return False

        if not self.validate_alias(self.alias):
            return False

        if not self.validate_password(self.password):
            return False

        return True

    def validate_user_login(self) -> bool:
        """Validate user login data."""
        if not self.validate_email(self.email):
            return False

        if not self.validate_password(self.password):
            return False

        return True

    def validate_user_no_password(self) -> bool:
        """Validate user data excluding password."""
        if not self.validate_email(self.email):
            return False

        if not self.validate_alias(self.alias):
            return False

        return True

    @staticmethod
    def validate_email(email: str) -> bool:
        """Check if email format is valid."""
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(email_pattern, email) is not None

    @staticmethod
    def validate_password(password: str) -> bool:
        """Validate the password against business rules."""
        return bool(password) and len(password) >= 8

    @staticmethod
    def validate_alias(alias: Optional[str]) -> bool:
        """Validate the alias against business rules."""
        return alias != None and bool(3 <= len(alias.strip()) <= 30)

    def to_dict_no_password(self) -> dict:
        """Convert user to dictionary excluding password."""
        return {
            "id": self.id,
            "email": self.email,
            "alias": self.alias,
            "photo_url": self.photo_url,
        }
