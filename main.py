from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from src.infraestructure.graphql.schema import schema
from src.infraestructure.graphql.context import get_context

app = FastAPI()
graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Authentication Service!"}
