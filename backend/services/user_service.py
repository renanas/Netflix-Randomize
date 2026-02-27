from backend.models.user import UserCreate, UserUpdate
from backend.repository.user_repository import UserRepository
from typing import Optional

class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    def create_user(self, user: UserCreate) -> str:
        """
        Create a new user via repository.
        """
        return self.user_repo.create_user(user)

    def get_all_users(self) -> list:
        """
        Get all users via repository.
        """
        return self.user_repo.get_all_users()

    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """
        Get a user by ID via repository.
        """
        return self.user_repo.get_user_by_id(user_id)

    def update_user(self, user_id: str, update_data: UserUpdate) -> bool:
        """
        Update a user by ID via repository.
        """
        return self.user_repo.update_user(user_id, update_data)

    def delete_user(self, user_id: str) -> bool:
        """
        Delete a user by ID via repository.
        """
        return self.user_repo.delete_user(user_id)

    def update_user_rating(self, user_id: str, tmdb_id: int, score: int) -> bool:
        """
        Add a rating to a user via repository.
        """
        return self.user_repo.add_user_rating(user_id, tmdb_id, score)

    def add_to_viewing_history(self, user_id: str, tmdb_id: int) -> bool:
        """
        Add a movie to user's viewing history via repository.
        """
        return self.user_repo.add_to_viewing_history(user_id, tmdb_id)

    def remove_from_viewing_history(self, user_id: str, tmdb_id: int) -> bool:
        """
        Remove a movie from user's viewing history via repository.
        """
        return self.user_repo.remove_from_viewing_history(user_id, tmdb_id)

    def update_playback_status(self, user_id: str, tmdb_id: int, seconds: int) -> bool:
        """
        Update playback status for a movie (pause time in seconds) via repository.
        """
        return self.user_repo.update_playback_status(user_id, tmdb_id, seconds)
