from pydantic import BaseModel, EmailStr, Field

class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    alias: str = Field(min_length=3, max_length=50)
    photo_url: str | None = None

class UserRegisterResponseSchema(BaseModel):
    user_id: str