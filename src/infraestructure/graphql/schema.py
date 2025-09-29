import strawberry
from strawberry.types import Info
from src.application.user_use_cases import UserUseCases
from src.application.token_use_cases import TokenUseCases
from .decorators import login_required
from src.infraestructure.graphql.types import (
    UserType,
    UserInput,
    TokenType,
    PasswordResetResponse,
    userInfoType,
    decodedTokenType,
)

# from src.infraestructure.repositories.in_memory_user_repository import InMemoryUserRepository
from src.infraestructure.repositories.firebase_user_repository import (
    FirebaseUserRepository,
)
from src.infraestructure.repositories.token_auth_repository import TokenAuthRepository

# Inyección de dependencias
# user_repository = InMemoryUserRepository()
user_repository = FirebaseUserRepository()
token_repository = TokenAuthRepository()
user_use_cases = UserUseCases(user_repository)
token_use_cases = TokenUseCases(token_repository)


@strawberry.type
class Query:
    @strawberry.field
    def get_user(self, user_id: str) -> UserType | None:
        user_data = user_use_cases.get_user(user_id)
        if user_data:
            return UserType(**user_data)
        return None

    @strawberry.field
    def list_users(self) -> list[UserType]:
        users_data = user_use_cases.list_users()
        return [UserType(**user) for user in users_data]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, user_input: UserInput) -> UserType:
        user_data = user_use_cases.create_user(
            email=user_input.email, password=user_input.password, alias=user_input.alias
        )
        return UserType(**user_data)

    @strawberry.mutation
    def login_user(self, email: str, password: str) -> TokenType | None:
        login_data = user_use_cases.login_user(email, password)
        if login_data:
            return TokenType(**login_data)
        return None

    @strawberry.mutation
    @login_required
    def update_user(self, info: Info, user_input: UserInput) -> UserType | None:
        decoded_token = info.context.get("verified_token")
        user_id = decoded_token.get("uid")
        user_data = {
            "id": user_id,
            "email": user_input.email,
            "password": user_input.password,
            "alias": user_input.alias,
        }
        updated_user = user_use_cases.update_user(user_data)
        if updated_user:
            return UserType(**updated_user)
        return None

    @strawberry.mutation
    def send_password_reset_email(self, email: str) -> PasswordResetResponse:
        reset_confirmation = user_use_cases.send_password_reset_email(email)
        return PasswordResetResponse(**reset_confirmation)

    @strawberry.mutation
    @login_required
    def delete_user(self, info: Info) -> bool:
        try:
            user_id = info.context.get("verified_token").get("uid")
            user_use_cases.delete_user(user_id)
            return True
        except Exception:
            return False

    @strawberry.mutation
    def verify_token(self, id_token: str) -> decodedTokenType | None:
        token_data = token_use_cases.verify_token(id_token)
        if token_data:
            return decodedTokenType(
                uid=token_data["uid"],
                email=token_data.get("email"),
                email_verified=token_data.get("email_verified"),
                user_info=userInfoType(**token_data.get("user_info")),
            )
        return None


schema = strawberry.Schema(query=Query, mutation=Mutation)
