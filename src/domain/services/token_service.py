from ..repositories.token_repository import TokenRepository
from ..entities.token import Token
from ..entities.refresh_token import RefreshToken
from typing import Optional


class TokenService:
    """Service layer for managing tokens, enforcing business rules."""

    def __init__(self, token_repository: TokenRepository):
        """Initialize the service with a token repository of some kind."""
        self.token_repository = token_repository

    def verify_token(self, id_token: str) -> Optional[Token]:
        """Verify a token."""
        return self.token_repository.verify_token(id_token)

    def refresh_token(self, refresh_token: str) -> RefreshToken:
        """Refresh an existing token."""
        return self.token_repository.refresh_token(refresh_token)
