import strawberry


@strawberry.type
class UserType:
    id: str
    email: str
    alias: str | None = None
    photo_url: str | None = None


@strawberry.input
class UserInput:
    email: str
    password: str
    alias: str | None = None


@strawberry.type
class TokenType:
    local_id: str
    email: str
    alias: str
    id_token: str
    registered: bool
    refresh_token: str
    expires_in: str


@strawberry.type
class PasswordResetResponse:
    success: bool
    response: str
