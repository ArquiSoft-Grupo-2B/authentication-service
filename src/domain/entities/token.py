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
