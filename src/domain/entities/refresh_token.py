from dataclasses import dataclass


@dataclass
class RefreshToken:
    access_token: str
    expires_in: str
    token_type: str
    refresh_token: str
    id_token: str
    user_id: str
    project_id: str

    def to_dict(self) -> dict:
        """Convert refresh token to dictionary."""
        return {
            "access_token": self.access_token,
            "expires_in": self.expires_in,
            "token_type": self.token_type,
            "refresh_token": self.refresh_token,
            "id_token": self.id_token,
            "user_id": self.user_id,
            "project_id": self.project_id,
        }
