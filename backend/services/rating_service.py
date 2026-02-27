
from backend.services.user_service import UserService


class RatingService:
    def __init__(self):
        self._user_service = None

    @property
    def user_service(self) -> UserService:
        """Lazy load UserService only when needed"""
        if self._user_service is None:
            self._user_service = UserService()
        return self._user_service

    def add_rating(self, user_id: str, tmdb_id: int, score: int):
        print(f"Adicionando nota para user: {user_id}, filme: {tmdb_id}")
        
        # Chama o serviço de usuário para atualizar o perfil dele
        response = self.user_service.update_user_rating(user_id, tmdb_id, score)
        return {"status": "success", "db_response": response}
