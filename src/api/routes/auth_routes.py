from fastapi import APIRouter, Depends, HTTPException, status
from src.application.user_use_cases import UserUseCases
from src.api.schemas.auth_schemas import UserCreateSchema, UserRegisterResponseSchema


router = APIRouter(prefix="/auth", tags=["auth"])

# Inject UserUseCases dependency
def get_user_use_cases() -> UserUseCases:
    from src.infraestructure.repositories.in_memory_user_repository import InMemoryUserRepository
    user_repository = InMemoryUserRepository()
    return UserUseCases(user_repository)

@router.get("/test")
def test_endpoint():
    return {"message": "Auth route is working!"}

@router.post("/register", response_model=UserRegisterResponseSchema, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreateSchema, user_use_cases: UserUseCases = Depends(get_user_use_cases)):
    try:
        user_id = user_use_cases.create_user(user_data.model_dump())
        return UserRegisterResponseSchema(user_id=user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))