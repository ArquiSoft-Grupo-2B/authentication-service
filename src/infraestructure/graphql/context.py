import strawberry
from strawberry.types import Info
from graphql import GraphQLError
from fastapi import Request


async def get_context(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header:
        header_parts = auth_header.split(" ")
        return {"auth_header": header_parts}
    else:
        return {"auth_header": ["", ""]}  # Default empty header parts
