from ..infraestructure.repositories.firebase_user_repository import (
    FirebaseUserRepository,
)
from ..infraestructure.repositories.token_auth_repository import TokenAuthRepository
from ..application.user_use_cases import UserUseCases
from ..application.token_use_cases import TokenUseCases


class FirebaseAdapter:
    def __init__(self):
        self.user_repository = FirebaseUserRepository()
        self.token_repository = TokenAuthRepository()
        self.user_use_cases = UserUseCases(self.user_repository)
        self.token_use_cases = TokenUseCases(self.token_repository)
