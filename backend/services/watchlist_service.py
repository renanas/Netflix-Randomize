from backend.repository.watchlist_repository import WatchlistRepository
from typing import List, Dict


class WatchlistService:
    """
    Service layer for watchlist operations.
    Handles business logic between routers and repositories.
    """
    
    def __init__(self):
        self.watchlist_repo = WatchlistRepository()
    
    def add_movie(self, user_id: str, tmdb_id: int) -> Dict[str, any]:
        """
        Add a movie to the user's watchlist.
        
        Raises:
            ValueError: If movie already in watchlist or doesn't exist in database.
        
        Returns:
            Dict with operation details and updated count.
        """
        self.watchlist_repo.add_movie_to_watchlist(user_id, tmdb_id)
        
        watchlist_count = self.watchlist_repo.get_watchlist_count(user_id)
        
        return {
            "message": "Movie added to watchlist",
            "tmdb_id": tmdb_id,
            "my_list_count": watchlist_count
        }
    
    def remove_movie(self, user_id: str, tmdb_id: int) -> Dict[str, any]:
        """
        Remove a movie from the user's watchlist.
        
        Raises:
            ValueError: If movie not in watchlist.
        
        Returns:
            Dict with operation details and updated count.
        """
        self.watchlist_repo.remove_movie_from_watchlist(user_id, tmdb_id)
        
        watchlist_count = self.watchlist_repo.get_watchlist_count(user_id)
        
        return {
            "message": "Movie removed from watchlist",
            "tmdb_id": tmdb_id,
            "my_list_count": watchlist_count
        }
    
    def get_watchlist(self, user_id: str) -> Dict[str, any]:
        """
        Get user's watchlist with movie IDs only.
        
        Returns:
            Dict with my_list (List[int]) and count.
        """
        my_list = self.watchlist_repo.get_watchlist(user_id)
        
        return {
            "my_list": my_list,
            "count": len(my_list)
        }
    
    def get_watchlist_detailed(self, user_id: str) -> Dict[str, any]:
        """
        Get user's watchlist with full movie details.
        
        Returns:
            Dict with my_list (List[dict] with movie info) and count.
        """
        my_list = self.watchlist_repo.get_watchlist_with_details(user_id)
        
        return {
            "my_list": my_list,
            "count": len(my_list)
        }
    
    def check_movie_in_watchlist(self, user_id: str, tmdb_id: int) -> Dict[str, any]:
        """
        Check if a specific movie is in the user's watchlist.
        
        Returns:
            Dict with tmdb_id and in_watchlist boolean flag.
        """
        in_watchlist = self.watchlist_repo.is_movie_in_watchlist(user_id, tmdb_id)
        
        return {
            "tmdb_id": tmdb_id,
            "in_watchlist": in_watchlist
        }
    
    def get_watchlist_count(self, user_id: str) -> int:
        """
        Get the total count of movies in the user's watchlist.
        
        Returns:
            Integer with the count of movies.
        """
        return self.watchlist_repo.get_watchlist_count(user_id)
