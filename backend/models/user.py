from pydantic import BaseModel, EmailStr
from typing import List, Dict, Optional
from datetime import datetime


class Preferences(BaseModel):
    favorite_genres: List[int]


class Profile(BaseModel):
    profile_name: str
    avatar: str
    age_rating: str
    preferred_language: str
    preferences: Preferences
    my_list: List[int]  # Movie IDs

class ViewingHistoryItem(BaseModel):
    movie_id: int
    watched_at: datetime


class UserBehavior(BaseModel):
    viewing_history: List[ViewingHistoryItem]
    playback_status: Dict[str, int]  # Movie ID (string): pause time (in seconds)
    ratings: Dict[str, int]  # Movie ID (string): 0 (dislike) or 1 (like)
    ignored_movies: List[int]  # Movie IDs the user has chosen to ignore

class User(BaseModel):
    email: EmailStr
    password: str  # Hashed password
    plan: str
    country: str
    profile: Profile
    user_behavior: UserBehavior

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    plan: str
    country: str
    profile: Profile
    user_behavior: UserBehavior

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    plan: Optional[str] = None
    country: Optional[str] = None
    profile: Optional[Profile] = None
    user_behavior: Optional[UserBehavior] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class PlayMovieRequest(BaseModel):
    tmdb_id: int

class PauseMovieRequest(BaseModel):
    tmdb_id: int
    seconds: int