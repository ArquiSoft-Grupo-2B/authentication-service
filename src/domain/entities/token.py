from dataclasses import dataclass


@dataclass
class Token:
    """
    Represents an authentication token.
    """

    local_id: str
    email: str
    alias: str
    id_token: str
    registered: bool
    refresh_token: str
    expires_in: str

    def to_dict(self) -> dict:
        """Convert token to dictionary."""
        return {
            "local_id": self.local_id,
            "email": self.email,
            "alias": self.alias,
            "id_token": self.id_token,
            "registered": self.registered,
            "refresh_token": self.refresh_token,
            "expires_in": self.expires_in,
        }
