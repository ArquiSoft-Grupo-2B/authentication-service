from ...domain.repositories.token_repository import TokenRepository
from ...domain.entities.token import Token
from typing import Optional
from firebase_admin import auth


class TokenAuthRepository(TokenRepository):

    def verify_token(self, id_token: str) -> Optional[Token]:
        # Implement token verification logic here
        try:
            decoded_token = auth.verify_id_token(id_token)
            print(f"Decoded token: {decoded_token}")
            return decoded_token
        except Exception as e:
            print(f"Token verification failed: {e}")
            return None

    def refresh_token(
        self, old_token_str: str, new_token_str: str, expires_in: int
    ) -> Token:
        # Implement token refresh logic here
        pass
