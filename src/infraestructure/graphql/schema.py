import strawberry
from src.application.user_use_cases import UserUseCases
from src.infraestructure.graphql.types import UserType, UserInput
# from src.infraestructure.repositories.in_memory_user_repository import InMemoryUserRepository
from src.infraestructure.repositories.firebase_user_repository import FirebaseUserRepository

# Inyección de dependencias
# user_repository = InMemoryUserRepository()
user_repository = FirebaseUserRepository()
user_use_cases = UserUseCases(user_repository)

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
            email=user_input.email,
            password=user_input.password,
            alias=user_input.alias
        )
        return UserType(**user_data)

    @strawberry.mutation
    def update_user(self, user_id: str, user_input: UserInput) -> UserType | None:
        user_data = {
            "id": user_id,
            "email": user_input.email,
            "password": user_input.password,
            "alias": user_input.alias
        }
        updated_user = user_use_cases.update_user(user_data)
        if updated_user:
            return UserType(**updated_user)
        return None

    @strawberry.mutation
    def delete_user(self, user_id: str) -> bool:
        try:
            user_use_cases.delete_user(user_id)
            return True
        except Exception:
            return False

schema = strawberry.Schema(query=Query, mutation=Mutation)