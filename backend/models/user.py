from pydantic import BaseModel, EmailStr
from typing import List, Dict

class Profile(BaseModel):
    profile_name: str
    avatar: str
    age_rating: str
    preferred_language: str
    my_list: List[int]  # Movie IDs

class UserBehavior(BaseModel):
    viewing_history: List[int]  # Movie IDs watched
    playback_status: Dict[str, int]  # Movie ID (string): pause time (in seconds)
    ratings: Dict[str, int]  # Movie ID (string): 0 (dislike) or 1 (like)
    favorite_genres: List[str]

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
    email: EmailStr = None
    password: str = None
    plan: str = None
    country: str = None
    profile: Profile = None
    user_behavior: UserBehavior = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str