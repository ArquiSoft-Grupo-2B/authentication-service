from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class User(BaseModel):
    id: str = Field(..., description="Identificador único del usuario")
    email: EmailStr
    alias: str
    password: str
    photo_url: Optional[str] = None

    def to_dict(self) -> dict:
        """Incluye la contraseña"""
        return self.model_dump()

    def to_dict_no_password(self) -> dict:
        """Excluye la contraseña"""
        return self.model_dump(exclude={"password"})
 