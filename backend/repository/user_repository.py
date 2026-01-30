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
        # Verificar se o email já existe
        existing_user = self.collection.find_one({"email": user.email})
        if existing_user:
            raise ValueError(f"Email {user.email} já está cadastrado")
        
        user_dict = user.dict()
        user_dict['senha'] = get_password_hash(user_dict['senha'])
        result = self.collection.insert_one(user_dict)
        return str(result.inserted_id)

    def _sanitize_user(self, user: dict) -> dict:
        if not user:
            return None
        # Convert ObjectId to string
        user = dict(user)
        if '_id' in user:
            try:
                user['_id'] = str(user['_id'])
            except Exception:
                pass
        # Remove sensitive fields
        user.pop('senha', None)
        return user

    def get_user_by_id(self, user_id: str) -> dict:
        """
        Get a user by ID.
        """
        user = self.collection.find_one({"_id": ObjectId(user_id)})
        return self._sanitize_user(user)

    def authenticate_user(self, email: str, password: str) -> dict:
        """
        Authenticate a user by email and password.
        Raises ValueError se o email não existir ou a senha for inválida.
        """
        user = self.collection.find_one({"email": email})
        if not user:
            raise ValueError(f"Email {email} não encontrado")
        if not verify_password(password, user.get('senha', '')):
            raise ValueError("Senha incorreta")
        return self._sanitize_user(user)

    def get_all_users(self) -> List[dict]:
        """
        Get all users.
        """
        users = list(self.collection.find())
        return [self._sanitize_user(u) for u in users]

    def update_user(self, user_id: str, update_data: UserUpdate) -> bool:
        """
        Update a user by ID.
        """
        update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
        # If updating password, hash it before saving
        if 'senha' in update_dict and update_dict['senha'] is not None:
            update_dict['senha'] = get_password_hash(update_dict['senha'])
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