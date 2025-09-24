from fastapi import FastAPI
from src.api.routes import auth_routes

app = FastAPI()
app.include_router(auth_routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Authentication Service!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)