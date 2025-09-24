from fastapi import APIRouter, Depends, HTTPException, status
from src.application.user_use_cases import UserUseCases
from src.api.schemas.auth_schemas import UserCreateSchema, UserRegisterResponseSchema
from functools import lru_cache


router = APIRouter(prefix="/auth", tags=["auth"])


# Inject UserUseCases dependency
@lru_cache()
def get_user_use_cases() -> UserUseCases:
    from src.infraestructure.repositories.in_memory_user_repository import (
        InMemoryUserRepository,
    )

    user_repository = InMemoryUserRepository()
    return UserUseCases(user_repository)


@router.get("/test")
def test_endpoint():
    return {"message": "Auth route is working!"}


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_data: UserCreateSchema,
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
):
    try:
        created_user = user_use_cases.create_user(
            email=user_data.email, password=user_data.password, alias=user_data.alias
        )
        return created_user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
