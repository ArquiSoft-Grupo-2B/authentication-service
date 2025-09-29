from abc import ABC, abstractmethod
from typing import Optional
from ..entities.token import Token


class TokenRepository(ABC):

    @abstractmethod
    def verify_token(self, id_token: str) -> Optional[Token]:
        pass

    @abstractmethod
    def refresh_token(
        self, old_token_str: str, new_token_str: str, expires_in: int
    ) -> Token:
        pass
