from dataclasses import dataclass
from typing import Optional


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
