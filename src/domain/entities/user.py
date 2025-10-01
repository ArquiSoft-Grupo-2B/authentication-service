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
    # display_name según firebase, alias según historia de usuario
    alias: Optional[str] = None
    photo_url: str | None = None

    def validate(
        self, exclude_password: bool = False, exclude_alias: bool = False
    ) -> bool:
        """Validate user data according to business rules."""
        if not self.email or not self._is_valid_email(self.email):
            return False

        if not exclude_alias and (
            self.alias is not None and len(self.alias.strip()) == 0
        ):
            return False

        if not exclude_password and (not self.password or len(self.password) < 8):
            return False

        return True

    def _is_valid_email(self, email: str) -> bool:
        """Check if email format is valid."""
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(email_pattern, email) is not None

    def to_dict_no_password(self) -> dict:
        """Convert user to dictionary excluding password."""
        return {
            "id": self.id,
            "email": self.email,
            "alias": self.alias,
            "photo_url": self.photo_url,
        }
