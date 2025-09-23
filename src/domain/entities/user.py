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
    display_name: Optional[str] = None
    phone: Optional[str] = None
    photo_url: str | None = None

    def validate(self) -> bool:
        """Validate user data according to business rules."""
        if not self.email or not self._is_valid_email(self.email):
            return False
        
        if self.display_name and len(self.display_name.strip()) == 0:
            return False
            
        return True
    
    def _is_valid_email(self, email: str) -> bool:
        """Check if email format is valid."""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None
