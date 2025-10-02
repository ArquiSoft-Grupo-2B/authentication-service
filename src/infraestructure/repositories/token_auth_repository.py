from ...domain.repositories.token_repository import TokenRepository
from ...domain.entities.token import Token
from ...domain.entities.refresh_token import RefreshToken
from typing import Optional
from firebase_admin import auth
from ..rest.firebase_auth_api import FirebaseAuthAPI


class TokenAuthRepository(TokenRepository):

    def verify_token(self, id_token: str) -> Optional[Token]:
        # Implement token verification logic here
        try:
            decoded_token = auth.verify_id_token(id_token)
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

    def refresh_token(self, refresh_token: str) -> RefreshToken:
        firebase_api = FirebaseAuthAPI()
        try:
            new_tokens = firebase_api.refresh_id_token(refresh_token)
            return new_tokens
        except ValueError as e:
            raise ValueError(f"Error refreshing token: {str(e)}")
