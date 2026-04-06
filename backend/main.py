from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers.movies_routers import router as movies_router
from backend.routers.users_routers import router as users_router
from backend.routers.auth_routers import router as auth_router
from backend.routers.watchlist_routers import router as watchlist_router
from backend.routers.rating_routers import router as rating_router
from backend.routers.playback_routers import router as playback_router
from backend.routers.recommendation_routers import router as recommendation_router
from backend.config import API_PREFIX

app = FastAPI(
    title="Netflix Clone API",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:3000", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the Netflix Clone API!"}

app.include_router(movies_router, prefix=API_PREFIX)
app.include_router(users_router, prefix=API_PREFIX)
app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(watchlist_router, prefix=API_PREFIX)
app.include_router(rating_router, prefix=API_PREFIX)
app.include_router(playback_router, prefix=API_PREFIX)
app.include_router(recommendation_router, prefix=API_PREFIX)