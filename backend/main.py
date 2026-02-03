from fastapi import FastAPI
from backend.routers.movies_routers import router as movies_router
from backend.routers.users_routers import router as users_router
from backend.routers.auth_routers import router as auth_router
from backend.routers.watchlist_routers import router as watchlist_router
from backend.config import API_PREFIX

app = FastAPI(
    title="Netflix Clone API",
    version="1.0.0",
)

@app.get("/")
def root():
    return {"message": "Welcome to the Netflix Clone API!"}

app.include_router(movies_router, prefix=API_PREFIX)
app.include_router(users_router, prefix=API_PREFIX)
app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(watchlist_router, prefix=API_PREFIX)