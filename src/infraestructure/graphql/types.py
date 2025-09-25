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
