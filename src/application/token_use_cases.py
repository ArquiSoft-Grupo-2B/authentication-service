from ..domain.repositories.token_repository import TokenRepository
from ..domain.entities.token import Token
from ..domain.entities.refresh_token import RefreshToken


class TokenUseCases:
    """Use cases for managing tokens, coordinating between service and repository layers."""

    def __init__(self, token_repository: TokenRepository):
        self.token_repository = token_repository

    def verify_token(self, id_token: str) -> dict | None:
        token: Token = self.token_repository.verify_token(id_token)
        return token.to_dict() if token else None

    def refresh_token(self, refresh_token: str) -> RefreshToken | None:
        refresh_token: RefreshToken = self.token_repository.refresh_token(refresh_token)
        return refresh_token if refresh_token else None
