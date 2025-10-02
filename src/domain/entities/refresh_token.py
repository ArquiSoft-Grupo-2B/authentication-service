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
