import sys
import types
from fastapi.testclient import TestClient

# Inject fake repository modules before importing the app to avoid real DB connections
fake_user_repo_mod = types.ModuleType("backend.repository.user_repository")
class FakeUserRepo:
    def __init__(self):
        self.users = {}

    def create_user(self, user):
        if user.email == "exists@example.com":
            raise ValueError("Email exists")
        uid = "user123"
        return uid

    def get_all_users(self):
        return [{"_id": "u1", "email": "a@example.com", "plan": "basic"}]

    def get_user_by_id(self, user_id: str):
        if user_id == "notfound":
            return None
        return {"_id": user_id, "email": "a@example.com", "plan": "basic"}

    def update_user(self, user_id: str, update_data):
        if user_id == "notfound":
            return False
        return True

    def delete_user(self, user_id: str):
        if user_id == "notfound":
            return False
        return True

    def authenticate_user(self, email: str, password: str):
        if email == "bad@example.com":
            raise ValueError("Invalid credentials")
        return {"_id": "u1", "email": email}


fake_user_repo_mod.UserRepository = FakeUserRepo
sys.modules["backend.repository.user_repository"] = fake_user_repo_mod

# minimal fake for movie_repository so imports succeed
fake_movie_repo_mod = types.ModuleType("backend.repository.movie_repository")
class FakeMovieRepo:
    def __init__(self):
        pass
fake_movie_repo_mod.MovieRepository = FakeMovieRepo
sys.modules["backend.repository.movie_repository"] = fake_movie_repo_mod

import backend.routers.users_routers as users_routers
import backend.routers.auth_routers as auth_routers
from fastapi import FastAPI

# Create a local FastAPI app and include routers so tests don't rely on global app import
app_local = FastAPI()
app_local.include_router(users_routers.router, prefix="")
app_local.include_router(auth_routers.router, prefix="")
client = TestClient(app_local)

# Inject fake repo into router modules
users_routers.user_repo = FakeUserRepo()
auth_routers.user_repo = users_routers.user_repo


def test_create_user_success():
    payload = {
        "email": "new@example.com",
        "password": "pass",
        "plan": "basic",
        "country": "BR",
        "profile": {
            "profile_name": "Main",
            "avatar": "a.png",
            "age_rating": "12",
            "preferred_language": "en",
            "my_list": []
        },
        "user_behavior": {
            "viewing_history": [],
            "playback_status": {},
            "ratings": {},
            "favorite_genres": []
        }
    }
    resp = client.post("/users", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "user_id" in data


def test_create_user_conflict():
    payload = {
        "email": "exists@example.com",
        "password": "pass",
        "plan": "basic",
        "country": "BR",
        "profile": {
            "profile_name": "Main",
            "avatar": "a.png",
            "age_rating": "12",
            "preferred_language": "en",
            "my_list": []
        },
        "user_behavior": {
            "viewing_history": [],
            "playback_status": {},
            "ratings": {},
            "favorite_genres": []
        }
    }
    resp = client.post("/users", json=payload)
    assert resp.status_code == 400


def test_get_all_users():
    resp = client.get("/users")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)


def test_get_user_not_found():
    resp = client.get("/users/notfound")
    assert resp.status_code == 404


def test_update_user_not_found():
    payload = {"plano": "premium"}
    resp = client.put("/users/notfound", json=payload)
    assert resp.status_code == 404


def test_delete_user_not_found():
    resp = client.delete("/users/notfound")
    assert resp.status_code == 404


def test_login_failure():
    payload = {"email": "bad@example.com", "password": "x"}
    resp = client.post("/login", json=payload)
    assert resp.status_code == 401
