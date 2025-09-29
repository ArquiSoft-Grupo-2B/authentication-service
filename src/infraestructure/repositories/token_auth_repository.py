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
            token_data = {
                "uid": decoded_token.get("uid"),
                "email": decoded_token.get("email"),
                "email_verified": decoded_token.get("email_verified"),
                "user_info": {
                    "name": decoded_token.get("name"),
                    "user_id": decoded_token.get("user_id"),
                },
            }
            return token_data

        except auth.ExpiredIdTokenError:
            raise ValueError("Expired token")
        except auth.InvalidIdTokenError:
            raise ValueError("Invalid token")
        except Exception as e:
            raise ValueError(f"Error verifying token: {str(e)}")

    def refresh_token(
        self, old_token_str: str, new_token_str: str, expires_in: int
    ) -> Token:
        # Implement token refresh logic here
        pass
