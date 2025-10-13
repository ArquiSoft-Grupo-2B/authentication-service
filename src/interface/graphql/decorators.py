import strawberry
from strawberry.types import Info
from graphql import GraphQLError
from ...infrastructure.repositories.token_auth_repository import TokenAuthRepository
from functools import wraps

token_repository = TokenAuthRepository()


def login_required(resolver):
    @wraps(resolver)
    def wrapper(*args, info: Info, **kwargs):
        context = info.context
        auth_header = context.get("auth_header")
        if auth_header[0].lower() != "bearer":
            raise GraphQLError(
                "Invalid authorization header",
                extensions={"code": "UNAUTHORIZED"},
            )
        token = auth_header[1]
        if not token:
            raise GraphQLError(
                "Authorization required", extensions={"code": "UNAUTHORIZED"}
            )
        try:
            verified_token = token_repository.verify_token(token)
            context["verified_token"] = verified_token
        except Exception as e:
            raise GraphQLError(f"{str(e)}", extensions={"code": "UNAUTHORIZED"})

        return resolver(*args, info=info, **kwargs)

    return wrapper
