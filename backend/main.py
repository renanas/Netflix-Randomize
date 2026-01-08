from fastapi import FastAPI
from backend.routers.movies_routers import router as movies_router
from backend.routers.users_routers import router as users_router

app = FastAPI(
    title="Netflix Clone API",
    version="1.0.0",
)

@app.get("/")
def root():
    return {"message": "Welcome to the Netflix Clone API!"}

app.include_router(movies_router)
app.include_router(users_router)