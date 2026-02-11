
from backend.services.user_service import UserService


class RatingService:
    def __init__(self, user_service: UserService):
        # O RatingService RECEBE o UserService pronto
        self.user_service = user_service

    def add_rating(self, user_id: str, tmdb_id: int, score: int):
        print(f"Adicionando nota para user: {user_id}, filme: {tmdb_id}")
        
        # Chama o serviço de usuário para atualizar o perfil dele
        response = self.user_service.update_user_rating(user_id, tmdb_id, score)
        return {"status": "success", "db_response": response}
