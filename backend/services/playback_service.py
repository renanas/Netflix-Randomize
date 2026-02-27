from backend.services.user_service import UserService


class PlaybackService:
    def __init__(self):
        self._user_service = None

    @property
    def user_service(self) -> UserService:
        """Lazy load UserService only when needed"""
        if self._user_service is None:
            self._user_service = UserService()
        return self._user_service

    def play_movie(self, user_id: str, tmdb_id: int) -> dict:
        """
        Start playing a movie - adds it to viewing history.
        """
        try:
            success = self.user_service.add_to_viewing_history(user_id, tmdb_id)
            if success:
                return {
                    "status": "success",
                    "message": f"Movie {tmdb_id} added to viewing history",
                    "tmdb_id": tmdb_id
                }
            else:
                return {
                    "status": "info",
                    "message": f"Movie {tmdb_id} is already in viewing history",
                    "tmdb_id": tmdb_id
                }
        except Exception as e:
            raise Exception(f"Error playing movie: {str(e)}")

    def pause_movie(self, user_id: str, tmdb_id: int, seconds: int) -> dict:
        """
        Pause a movie - removes from viewing history and saves playback status.
        """
        try:
            # Remove from viewing history
            self.user_service.remove_from_viewing_history(user_id, tmdb_id)
            
            # Update playback status with pause time
            success = self.user_service.update_playback_status(user_id, tmdb_id, seconds)
            
            if success:
                return {
                    "status": "success",
                    "message": f"Movie {tmdb_id} paused at {seconds} seconds",
                    "tmdb_id": tmdb_id,
                    "pause_seconds": seconds
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to update playback status for movie {tmdb_id}",
                    "tmdb_id": tmdb_id
                }
        except Exception as e:
            raise Exception(f"Error pausing movie: {str(e)}")
