from backend.database.mongodb_connection import MongoDBConnection
from backend.models.user import User, UserCreate, UserUpdate
from backend.utils.auth import get_password_hash, verify_password
from bson import ObjectId
from typing import List

class UserRepository:
    def __init__(self):
        self.mongo_conn = MongoDBConnection()
        self.mongo_conn.connect()
        self.db = self.mongo_conn.get_db()
        self.collection = self.db["users"]

    def create_user(self, user: UserCreate) -> str:
        """
        Create a new user in the database.
        """
        user_dict = user.dict()
        user_dict['senha'] = get_password_hash(user_dict['senha'])
        result = self.collection.insert_one(user_dict)
        return str(result.inserted_id)

    def get_user_by_id(self, user_id: str) -> dict:
        """
        Get a user by ID.
        """
        return self.collection.find_one({"_id": ObjectId(user_id)})

    def authenticate_user(self, email: str, password: str) -> dict:
        """
        Authenticate a user by email and password.
        """
        user = self.collection.find_one({"email": email})
        if user and verify_password(password, user['senha']):
            return user
        return None

    def get_all_users(self) -> List[dict]:
        """
        Get all users.
        """
        return list(self.collection.find())

    def update_user(self, user_id: str, update_data: UserUpdate) -> bool:
        """
        Update a user by ID.
        """
        update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
        if not update_dict:
            return False
        result = self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_dict})
        return result.modified_count > 0

    def delete_user(self, user_id: str) -> bool:
        """
        Soft delete a user by setting a 'deleted' flag.
        """
        result = self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"deleted": True}})
        return result.modified_count > 0