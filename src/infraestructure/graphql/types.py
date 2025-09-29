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
class TokenRefreshType:
    access_token: str
    expires_in: str
    token_type: str
    refresh_token: str
    id_token: str
    user_id: str
    project_id: str


@strawberry.type
class userInfoType:
    name: str
    user_id: str


@strawberry.type
class decodedTokenType:
    uid: str
    email: str
    email_verified: bool
    user_info: userInfoType


@strawberry.type
class PasswordResetResponse:
    success: bool
    response: str
