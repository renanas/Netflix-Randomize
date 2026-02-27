from backend.database.mongodb_connection import MongoDBConnection
from backend.models.user import User, UserCreate, UserUpdate
from backend.utils.auth import get_password_hash, verify_password
from bson import ObjectId
from typing import List, Optional

class UserRepository:
    def __init__(self):
        self.mongo_conn = MongoDBConnection()
        if not self.mongo_conn.connect():
            raise RuntimeError("Failed to connect to MongoDB")
        self.db = self.mongo_conn.get_db()
        if self.db is None:
            raise RuntimeError("Database connection failed: db is None")
        self.collection = self.db["users"]

    def create_user(self, user: UserCreate) -> str:
        """
        Create a new user in the database.
        """
        # Check if email already exists
        existing_user = self.collection.find_one({"email": user.email})
        if existing_user:
            raise ValueError(f"Email {user.email} is already registered")
        
        user_dict = user.dict()
        user_dict['password'] = get_password_hash(user_dict['password'])
        result = self.collection.insert_one(user_dict)
        return str(result.inserted_id)

    def _sanitize_user(self, user: Optional[dict]) -> Optional[dict]:
        if not user:
            return None
        # Convert ObjectId to string
        user = dict(user)
        if '_id' in user:
            try:
                user['_id'] = str(user['_id'])
            except Exception:
                pass
        # Remove sensitive fields (password)
        user.pop('password', None)
        return user

    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """
        Get a user by ID.
        """
        user = self.collection.find_one({"_id": ObjectId(user_id)})
        return self._sanitize_user(user)

    def authenticate_user(self, email: str, password: str) -> Optional[dict]:
        """
        Authenticate a user by email and password.
        Raises ValueError if email is not found or password is invalid.
        """
        user = self.collection.find_one({"email": email})
        if not user:
            raise ValueError(f"Email {email} not found")
        if not verify_password(password, user.get('password', '')):
            raise ValueError("Invalid password")
        return self._sanitize_user(user)

    def get_all_users(self) -> List[dict]:
        """
        Get all users.
        """
        users = list(self.collection.find())
        return [sanitized for u in users if (sanitized := self._sanitize_user(u)) is not None]

    def update_user(self, user_id: str, update_data: UserUpdate) -> bool:
        """
        Update a user by ID.
        """
        update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
        # If updating password, hash it before saving
        if 'password' in update_dict and update_dict['password'] is not None:
            update_dict['password'] = get_password_hash(update_dict['password'])
        if not update_dict:
            return False
        result = self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_dict})
        return result.modified_count > 0
    
    def add_user_rating(self, user_id: str, tmdb_id: int, score: int) -> bool:
        # Usando a Dot Notation para acessar user_behavior.ratings.ID
        # Aqui definimos o valor como True, ou a nota numérica
        field_path = f"user_behavior.ratings.{tmdb_id}"
        
        result = self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {field_path: score}} # Ou a nota que desejar
        )
        return result.modified_count > 0

    def delete_user(self, user_id: str) -> bool:
        """
        Soft delete a user by setting a 'deleted' flag.
        """
        result = self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"deleted": True}})
        return result.modified_count > 0

    def add_to_viewing_history(self, user_id: str, tmdb_id: int) -> bool:
        """
        Add a movie to user's viewing history.
        Avoids duplicates by checking if already exists.
        """
        field_path = "user_behavior.viewing_history"
        result = self.collection.update_one(
            {"_id": ObjectId(user_id), f"{field_path}": {"$ne": tmdb_id}},
            {"$push": {field_path: tmdb_id}}
        )
        return result.modified_count > 0 or result.matched_count > 0

    def remove_from_viewing_history(self, user_id: str, tmdb_id: int) -> bool:
        """
        Remove a movie from user's viewing history.
        """
        field_path = "user_behavior.viewing_history"
        result = self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$pull": {field_path: tmdb_id}}
        )
        return result.modified_count > 0

    def update_playback_status(self, user_id: str, tmdb_id: int, seconds: int) -> bool:
        """
        Update playback status for a movie (pause time in seconds).
        """
        field_path = f"user_behavior.playback_status.{tmdb_id}"
        result = self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {field_path: seconds}}
        )
        return result.modified_count > 0