from abc import ABC, abstractmethod
from typing import Optional
from ..entities.token import Token
from ..entities.refresh_token import RefreshToken


class TokenRepository(ABC):

    @abstractmethod
    def verify_token(self, id_token: str) -> Optional[Token]:
        pass

    @abstractmethod
    def refresh_token(self, refresh_token: str) -> RefreshToken:
        pass
