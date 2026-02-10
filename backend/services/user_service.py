from backend.models.user import UserCreate, UserUpdate
from backend.repository.user_repository import UserRepository

class UserService:

    def __init__(self):
        self.user_repo = UserRepository()


    def update_user(self, user_id: str, update_data: UserUpdate):
        self.user_repo.update_user(user_id, update_data)

