import sys
import os
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Ensure backend is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pymongo import MongoClient

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
MODEL_PATH = os.path.join(MODEL_DIR, 'knn_model.pkl')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.pkl')
METADATA_PATH = os.path.join(MODEL_DIR, 'movie_metadata.pkl')

# Cache loaded model to avoid reloading
_LOADED_MODEL = None
_LOADED_SCALER = None
_LOADED_METADATA = None


def load_model():
    """Load pre-trained KNN model and metadata."""
    global _LOADED_MODEL, _LOADED_SCALER, _LOADED_METADATA
    
    if _LOADED_MODEL is not None:
        return _LOADED_MODEL, _LOADED_SCALER, _LOADED_METADATA
    
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Run train_model.py first.")
    if not os.path.exists(SCALER_PATH):
        raise FileNotFoundError(f"Scaler not found at {SCALER_PATH}. Run train_model.py first.")
    if not os.path.exists(METADATA_PATH):
        raise FileNotFoundError(f"Metadata not found at {METADATA_PATH}. Run train_model.py first.")
    
    _LOADED_MODEL = joblib.load(MODEL_PATH)
    _LOADED_SCALER = joblib.load(SCALER_PATH)
    _LOADED_METADATA = joblib.load(METADATA_PATH)
    
    logger.info("Model, scaler, and metadata loaded successfully")
    return _LOADED_MODEL, _LOADED_SCALER, _LOADED_METADATA


def get_mongo_connection():
    """Connect to MongoDB."""
    uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME", "netflix")
    if not uri:
        raise ValueError("MONGO_URI not set in .env")
    
    client = MongoClient(uri)
    db = client[db_name]
    return db


def build_movie_feature_vector(movie: dict, metadata: dict) -> np.ndarray:
    """Build feature vector for a single movie."""
    genre_id_to_index = metadata['genre_id_to_index']
    
    # One-hot encode genres
    genre_feature = np.zeros(len(genre_id_to_index))
    genre_ids = movie.get("genre_ids", []) or []
    if isinstance(genre_ids, list):
        for gid in genre_ids:
            if gid in genre_id_to_index:
                genre_feature[genre_id_to_index[gid]] = 1
    
    # Scalar features
    popularity = float(movie.get("popularity", 0) or 0)
    vote_avg = float(movie.get("vote_average", 0) or 0)
    vote_count = float(movie.get("vote_count", 0) or 0)
    vote_count_log = np.log1p(vote_count)
    
    feature_vector = np.concatenate([
        genre_feature,
        [popularity, vote_avg, vote_count_log]
    ])
    
    return feature_vector


def recommend_similar_movies_with_data(
    reference_movies: list,
    exclude_ids: set = None,
    n_recommendations: int = 20,
    return_distances: bool = False
):
    """
    Find movies similar to reference movies using trained KNN.
    Works with pre-loaded movie data (for testing and service integration).
    
    Args:
        reference_movies: List of movie dicts (TMDB format) to base recommendation on
        exclude_ids: Set of movie IDs to exclude (already watched, rated, etc)
        n_recommendations: Number of recommendations to return
        return_distances: If True, return (movie_id, distance) tuples
    
    Returns:
        List of recommended movie IDs (or tuples with distances)
    """
    knn_model, scaler, metadata = load_model()
    movie_ids = metadata['movie_ids']
    movie_id_to_idx = {mid: idx for idx, mid in enumerate(movie_ids)}
    
    if exclude_ids is None:
        exclude_ids = set()
    
    # Build average feature vector from reference movies
    reference_vectors = []
    for ref_movie in reference_movies:
        ref_id = ref_movie.get("id")
        if ref_id not in movie_id_to_idx:
            continue
        feature_vec = build_movie_feature_vector(ref_movie, metadata)
        reference_vectors.append(feature_vec)
    
    if not reference_vectors:
        return []
    
    avg_feature_vector = np.mean(reference_vectors, axis=0)
    scaled_vector = scaler.transform([avg_feature_vector])[0]
    
    # Find k nearest neighbors (we need more than n_recommendations to account for exclusions)
    k_search = min(n_recommendations * 3, len(movie_ids))
    distances, indices = knn_model.kneighbors([scaled_vector], n_neighbors=k_search)
    
    recommended_ids = []
    for idx, distance in zip(indices[0], distances[0]):
        movie_id = movie_ids[idx]
        if movie_id not in exclude_ids:
            recommended_ids.append((movie_id, float(distance)) if return_distances else movie_id)
            if len(recommended_ids) >= n_recommendations:
                break
    
    return recommended_ids


def recommend_similar_movies(
    reference_movie_ids: list,
    exclude_ids: set = None,
    n_recommendations: int = 20,
    return_distances: bool = False
):
    """
    Find movies similar to reference movies using trained KNN.
    
    Args:
        reference_movie_ids: List of movie IDs to base recommendation on
        exclude_ids: Set of movie IDs to exclude (already watched, rated, etc)
        n_recommendations: Number of recommendations to return
        return_distances: If True, return (movie_id, distance) tuples
    
    Returns:
        List of recommended movie IDs (or tuples with distances)
    """
    knn_model, scaler, metadata = load_model()
    movie_ids = metadata['movie_ids']
    movie_id_to_idx = {mid: idx for idx, mid in enumerate(movie_ids)}
    
    db = get_mongo_connection()
    movies_collection = db["movies"]
    
    if exclude_ids is None:
        exclude_ids = set()
    
    # Build average feature vector from reference movies
    reference_vectors = []
    for ref_id in reference_movie_ids:
        if ref_id not in movie_id_to_idx:
            continue
        ref_movie = movies_collection.find_one({"id": ref_id})
        if ref_movie:
            feature_vec = build_movie_feature_vector(ref_movie, metadata)
            reference_vectors.append(feature_vec)
    
    if not reference_vectors:
        return []
    
    avg_feature_vector = np.mean(reference_vectors, axis=0)
    scaled_vector = scaler.transform([avg_feature_vector])[0]
    
    # Find k nearest neighbors (we need more than n_recommendations to account for exclusions)
    k_search = min(n_recommendations * 3, len(movie_ids))
    distances, indices = knn_model.kneighbors([scaled_vector], n_neighbors=k_search)
    
    recommended_ids = []
    for idx, distance in zip(indices[0], distances[0]):
        movie_id = movie_ids[idx]
        if movie_id not in exclude_ids:
            recommended_ids.append((movie_id, float(distance)) if return_distances else movie_id)
            if len(recommended_ids) >= n_recommendations:
                break
    
    return recommended_ids


def recommend_for_user(user_id: str, n_recommendations: int = 20):
    """
    High-level recommendation for a user based on their history.
    
    Args:
        user_id: User ID
        n_recommendations: Number of recommendations
    
    Returns:
        List of recommended movie IDs
    """
    db = get_mongo_connection()
    users_collection = db["users"]
    
    user = users_collection.find_one({"_id": user_id})
    if not user:
        raise ValueError(f"User {user_id} not found")
    
    user_behavior = user.get("user_behavior", {}) or {}
    viewing_history = user_behavior.get("viewing_history", []) or []
    ratings = user_behavior.get("ratings", {}) or {}
    
    # Extract movie IDs from history
    watched_movie_ids = []
    for item in viewing_history:
        if isinstance(item, dict) and "movie_id" in item:
            watched_movie_ids.append(item["movie_id"])
    
    # Build exclude set
    exclude_ids = set(watched_movie_ids)
    exclude_ids.update(ratings.keys())
    
    if not watched_movie_ids:
        # If user has no history, return popular movies
        movies_collection = db["movies"]
        popular = list(movies_collection.find({}).sort("popularity", -1).limit(n_recommendations))
        return [m["id"] for m in popular if m.get("id") not in exclude_ids][:n_recommendations]
    
    # Use KNN to find similar movies
    recommendations = recommend_similar_movies(
        watched_movie_ids,
        exclude_ids=exclude_ids,
        n_recommendations=n_recommendations,
        return_distances=False
    )
    
    return recommendations
