from backend.database.mongodb_connection import MongoDBConnection
from bson import ObjectId
from typing import List


class WatchlistRepository:
    def __init__(self):
        self.mongo_conn = MongoDBConnection()
        self.mongo_conn.connect()
        self.db = self.mongo_conn.get_db()
        self.users_collection = self.db["users"]
        self.movies_collection = self.db["movies"]

    def add_movie_to_watchlist(self, user_id: str, tmdb_id: int) -> bool:
        """
        Add a movie to user's watchlist.
        Returns True if successful, raises ValueError if movie already in list or doesn't exist.
        """
        # Validate that the movie exists in the database
        movie = self.movies_collection.find_one({"id": tmdb_id})
        if not movie:
            raise ValueError(f"Movie with TMDB ID {tmdb_id} not found in database")

        try:
            # Check if movie is already in the user's watchlist
            user = self.users_collection.find_one(
                {
                    "_id": ObjectId(user_id),
                    "profile.my_list": tmdb_id
                }
            )
            if user:
                raise ValueError(f"Movie {tmdb_id} is already in your watchlist")

            # Add movie to watchlist
            result = self.users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$push": {"profile.my_list": tmdb_id}}
            )
            return result.modified_count > 0
        except Exception:
            raise ValueError("Invalid user ID")

    def remove_movie_from_watchlist(self, user_id: str, tmdb_id: int) -> bool:
        """
        Remove a movie from user's watchlist.
        Returns True if successful, raises ValueError if movie not in list.
        """
        try:
            # Check if movie is in the user's watchlist
            user = self.users_collection.find_one(
                {
                    "_id": ObjectId(user_id),
                    "profile.my_list": tmdb_id
                }
            )
            if not user:
                raise ValueError(f"Movie {tmdb_id} not found in your watchlist")

            # Remove movie from watchlist
            result = self.users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$pull": {"profile.my_list": tmdb_id}}
            )
            return result.modified_count > 0
        except Exception:
            raise ValueError("Invalid user ID")

    def get_watchlist(self, user_id: str) -> List[int]:
        """
        Get all movie IDs from user's watchlist.
        Returns an empty list if user has no movies.
        """
        try:
            user = self.users_collection.find_one(
                {"_id": ObjectId(user_id)},
                {"profile.my_list": 1}
            )
        except Exception:
            return []
        if not user or "profile" not in user or "my_list" not in user["profile"]:
            return []
        return user["profile"]["my_list"]

    def get_watchlist_with_details(self, user_id: str) -> List[dict]:
        """
        Get watchlist with full movie details from the movies collection.
        Returns a list of movie objects with title, poster, release_date, etc.
        """
        watchlist_ids = self.get_watchlist(user_id)
        if not watchlist_ids:
            return []

        movies = list(
            self.movies_collection.find(
                {"id": {"$in": watchlist_ids}},
                {
                    "id": 1,
                    "title": 1,
                    "poster_path": 1,
                    "release_date": 1,
                    "overview": 1,
                    "vote_average": 1
                }
            )
        )
        return movies

    def is_movie_in_watchlist(self, user_id: str, tmdb_id: int) -> bool:
        """
        Check if a movie is in the user's watchlist.
        """
        user = self.users_collection.find_one(
            {
                "_id": ObjectId(user_id),
                "profile.my_list": tmdb_id
            }
        )
        return user is not None

    def get_watchlist_count(self, user_id: str) -> int:
        """
        Get the total number of movies in the user's watchlist.
        """
        watchlist = self.get_watchlist(user_id)
        return len(watchlist)
