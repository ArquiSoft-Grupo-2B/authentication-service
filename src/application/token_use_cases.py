from ..domain.services.token_service import TokenService
from ..domain.repositories.token_repository import TokenRepository
from typing import Optional


class TokenUseCases:
    """Use cases for managing tokens, coordinating between service and repository layers."""

    def __init__(self, token_repository: TokenRepository):
        self.token_service = TokenService(token_repository)

    def verify_token(self, id_token: str) -> Optional[dict]:
        token = self.token_service.verify_token(id_token)
        return token if token else None

    def refresh_token(self, refresh_token: str) -> dict:
        token = self.token_service.refresh_token(refresh_token)
        return token
