from backend.models.user import UserCreate, UserUpdate
from backend.repository.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    def update_user_rating(self, user_id: str, tmdb_id: int, score: int):
        # Chama o novo método específico do repositório
        return self.user_repo.add_user_rating(user_id, tmdb_id, score)
