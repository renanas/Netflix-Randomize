import sys
import os
import types
from fastapi.testclient import TestClient

# ensure project root is on path for imports of backend package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Stub repository modules to avoid DB connection during import
fake_user_repo_mod = types.ModuleType("backend.repository.user_repository")
class FakeUserRepo:
    def __init__(self):
        pass
fake_user_repo_mod.UserRepository = FakeUserRepo
sys.modules["backend.repository.user_repository"] = fake_user_repo_mod

fake_movie_repo_mod = types.ModuleType("backend.repository.movie_repository")
class FakeMovieRepo:
    def __init__(self):
        pass
fake_movie_repo_mod.MovieRepository = FakeMovieRepo
sys.modules["backend.repository.movie_repository"] = fake_movie_repo_mod

import backend.routers.movies_routers as movies_routers
from fastapi import FastAPI

# Use a local app to avoid importing backend.main which may initialize DB connections
app_local = FastAPI()
app_local.include_router(movies_routers.router, prefix="")
client = TestClient(app_local)

# Replace the TMDB fetch functions with ones that raise
movies_routers.fetch_popular_movies = lambda page=1: (_ for _ in ()).throw(Exception("tmdb error"))
movies_routers.fetch_movie_details = lambda movie_id: (_ for _ in ()).throw(Exception("tmdb error"))


def test_fetch_popular_error():
    resp = client.get("/fetch-popular")
    assert resp.status_code == 500


def test_movie_details_error():
    resp = client.get("/movie/123")
    assert resp.status_code == 500
