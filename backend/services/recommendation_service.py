import sys
import os
from backend.services.user_service import UserService

# Add recommendation_system to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


class RecommendationService:
    def __init__(self):
        # import lazily to allow tests to patch sys.modules before instantiation
        from backend.repository.movie_repository import MovieRepository
        from backend.repository.recommendation_repository import RecommendationRepository

        self.user_service = UserService()
        self.movie_repository = MovieRepository()
        self.recommendation_repository = RecommendationRepository()
        
        # Load ML model (KNN) - REQUIRED
        try:
            from recommendation_system.recommend import load_model
            load_model()  # Warm up the model cache
        except Exception as e:
            raise RuntimeError(f"KNN model unavailable: {e}. Run: python scripts/train_recommendations.py")



    def build_recommendations_for_user(self, user_id: str, limit: int = 20):
        """Build recommendations using KNN model."""
        try:
            from recommendation_system.recommend import recommend_similar_movies_with_data
            
            # Get user data via injected UserService (allows test mocking)
            user = self.user_service.get_user_by_id(user_id)
            if not user:
                # No user found: return popular movies
                pop_movies = self.movie_repository.find_movies(limit=limit)
                movie_ids = [m.get("id") for m in pop_movies if m and m.get("id")]
                self.recommendation_repository.upsert_recommendations(user_id, movie_ids[:limit])
                return pop_movies[:limit]
            
            # Extract viewing history
            user_behavior = user.get("user_behavior", {}) or {}
            viewing_history = user_behavior.get("viewing_history", []) or []
            ratings = user_behavior.get("ratings", {}) or {}
            
            # Build watched and exclude sets
            watched_movie_ids = []
            for item in viewing_history:
                if isinstance(item, dict) and "movie_id" in item:
                    watched_movie_ids.append(item["movie_id"])
            
            exclude_ids = set(watched_movie_ids)
            # Convert rating keys to int to match movie IDs (which are ints)
            for rating_id in ratings.keys():
                try:
                    exclude_ids.add(int(rating_id))
                except (ValueError, TypeError):
                    exclude_ids.add(rating_id)
            
            # If user has no history, return popular movies
            if not watched_movie_ids:
                pop_movies = self.movie_repository.find_movies(limit=limit)
                movie_ids = [m.get("id") for m in pop_movies if m and m.get("id") and m.get("id") not in exclude_ids][:limit]
                self.recommendation_repository.upsert_recommendations(user_id, movie_ids)
                pop_movies_by_id = {m.get("id"): m for m in pop_movies if m and m.get("id")}
                return [pop_movies_by_id[mid] for mid in movie_ids if mid in pop_movies_by_id]
            
            # Fetch the watched movies from repository
            watched_movies = self.movie_repository.find_movies({"id": {"$in": watched_movie_ids}})
            watched_movies = [m for m in watched_movies if m and m.get("id")]
            
            if not watched_movies:
                # No watched movies found in repo (shouldn't happen), return popular
                pop_movies = self.movie_repository.find_movies(limit=limit)
                movie_ids = [m.get("id") for m in pop_movies if m and m.get("id") and m.get("id") not in exclude_ids][:limit]
                self.recommendation_repository.upsert_recommendations(user_id, movie_ids)
                return pop_movies[:limit]
            
            # Use KNN to find similar movies
            movie_ids = recommend_similar_movies_with_data(
                reference_movies=watched_movies,
                exclude_ids=exclude_ids,
                n_recommendations=limit,
                return_distances=False
            )
            
            # Fetch movie details from repository
            candidates = self.movie_repository.find_movies({"id": {"$in": movie_ids}}, limit=len(movie_ids))
            movie_by_id = {m.get("id"): m for m in candidates if m and m.get("id")}
            recommendations = [movie_by_id[mid] for mid in movie_ids if mid in movie_by_id]
            
            # Cache results
            self.recommendation_repository.upsert_recommendations(user_id, movie_ids)
            
            return recommendations
        except Exception as e:
            raise RuntimeError(f"KNN recommendation failed: {e}")



    def get_cached_recommendations(self, user_id: str, limit: int = 20):
        """Get cached recommendations from MongoDB."""
        movie_ids = self.recommendation_repository.get_recommendations(user_id) or []
        if not movie_ids:
            return None

        candidates = self.movie_repository.find_movies({"id": {"$in": movie_ids}}, limit=len(movie_ids))
        cand_by_id = {m.get("id"): m for m in candidates if m and m.get("id") is not None}

        ordered = [cand_by_id[mid] for mid in movie_ids if mid in cand_by_id]
        return ordered[:limit]

    def recommend_movies_for_user(self, user_id: str, min_recommendations: int = 3, force_refresh: bool = False):
        """
        Main entry point for recommendations (KNN-powered).
        
        Strategy:
        1. If force_refresh=True, regenerate recommendations using KNN
        2. If cache has enough recommendations, return cached
        3. If cache is empty or insufficient (cold start), use KNN to generate
        
        Args:
            user_id: User ID
            min_recommendations: Minimum recommendations to return (default 3)
            force_refresh: Force rebuild of recommendations (default False)
        
        Returns:
            List of recommended movies (dict objects with TMDB metadata)
            
        Resolves cold start: KNN generates recommendations for new users
        """
        limit = max(min_recommendations, 20)
        
        # Force refresh
        if force_refresh:
            return self.build_recommendations_for_user(user_id, limit=limit)
        
        # Try cached first
        cached = self.get_cached_recommendations(user_id, limit=limit)
        if cached and len(cached) >= min_recommendations:
            return cached[:limit]
        
        # Cold start or cache expired: generate new recommendations via KNN
        return self.build_recommendations_for_user(user_id, limit=limit)

