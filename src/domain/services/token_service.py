from ..repositories.token_repository import TokenRepository
from ..entities.token import Token
from typing import Optional


class TokenService:
    """Service layer for managing tokens, enforcing business rules."""

    def __init__(self, token_repository: TokenRepository):
        """Initialize the service with a token repository of some kind."""
        self.token_repository = token_repository

    def verify_token(self, id_token: str) -> Optional[Token]:
        """Verify a token."""
        return self.token_repository.verify_token(id_token)

    def refresh_token(
        self, old_token_str: str, new_token_str: str, expires_in: int
    ) -> Token:
        """Refresh an existing token."""
        return self.token_repository.refresh_token(
            old_token_str, new_token_str, expires_in
        )
