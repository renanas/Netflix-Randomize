import sys
import os
import numpy as np
import joblib
from pymongo import MongoClient
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Ensure backend is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
MODEL_PATH = os.path.join(MODEL_DIR, 'knn_model.pkl')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.pkl')
METADATA_PATH = os.path.join(MODEL_DIR, 'movie_metadata.pkl')

os.makedirs(MODEL_DIR, exist_ok=True)


def get_mongo_connection():
    """Connect to MongoDB and fetch all movies."""
    uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME", "netflix")
    if not uri:
        raise ValueError("MONGO_URI not set in .env")
    
    client = MongoClient(uri)
    db = client[db_name]
    return db


def extract_features(movies: list):
    """
    Extract features from movies for KNN training.
    
    Features:
    - genre_ids (one-hot encoded)
    - popularity (normalized)
    - vote_average (normalized)
    - vote_count (normalized with log scale)
    
    Returns:
    - feature_matrix: (n_movies, n_features)
    - movie_ids_list: list of movie IDs (aligned with rows)
    - genre_id_to_index: dict mapping genre_id to one-hot position
    """
    if not movies:
        raise ValueError("No movies provided for training")
    
    # Collect all unique genre IDs
    all_genre_ids = set()
    for movie in movies:
        genre_ids = movie.get("genre_ids", []) or []
        if isinstance(genre_ids, list):
            all_genre_ids.update(genre_ids)
    
    all_genre_ids = sorted(list(all_genre_ids))
    genre_id_to_index = {gid: idx for idx, gid in enumerate(all_genre_ids)}
    
    features_list = []
    movie_ids_list = []
    valid_movies = []
    
    for movie in movies:
        movie_id = movie.get("id")
        if not movie_id:
            continue
        
        # One-hot encode genres
        genre_feature = np.zeros(len(all_genre_ids))
        genre_ids = movie.get("genre_ids", []) or []
        if isinstance(genre_ids, list):
            for gid in genre_ids:
                if gid in genre_id_to_index:
                    genre_feature[genre_id_to_index[gid]] = 1
        
        # Scalar features
        popularity = float(movie.get("popularity", 0) or 0)
        vote_avg = float(movie.get("vote_average", 0) or 0)
        vote_count = float(movie.get("vote_count", 0) or 0)
        
        # Log scale for vote_count (avoid skew)
        vote_count_log = np.log1p(vote_count)
        
        # Combine all features
        feature_vector = np.concatenate([
            genre_feature,
            [popularity, vote_avg, vote_count_log]
        ])
        
        features_list.append(feature_vector)
        movie_ids_list.append(movie_id)
        valid_movies.append(movie)
    
    if not features_list:
        raise ValueError("No valid movies extracted for training")
    
    feature_matrix = np.array(features_list)
    
    return feature_matrix, movie_ids_list, genre_id_to_index, all_genre_ids, valid_movies


def train_knn_model(n_neighbors: int = 10):
    """
    Train KNN model on TMDB movies from MongoDB.
    
    Args:
        n_neighbors: Number of neighbors for KNN
    """
    logger.info("Connecting to MongoDB...")
    db = get_mongo_connection()
    movies_collection = db["movies"]
    
    logger.info("Fetching all movies from database...")
    all_movies = list(movies_collection.find({}, limit=5000))
    logger.info(f"Found {len(all_movies)} movies")
    
    logger.info("Extracting features...")
    feature_matrix, movie_ids_list, genre_id_to_index, all_genre_ids, valid_movies = extract_features(all_movies)
    logger.info(f"Feature matrix shape: {feature_matrix.shape}")
    
    logger.info("Standardizing features...")
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(feature_matrix)
    
    logger.info(f"Training KNN with {n_neighbors} neighbors...")
    knn_model = NearestNeighbors(n_neighbors=n_neighbors, metric='cosine', n_jobs=-1)
    knn_model.fit(scaled_features)
    
    logger.info(f"Saving model to {MODEL_PATH}")
    joblib.dump(knn_model, MODEL_PATH)
    
    logger.info(f"Saving scaler to {SCALER_PATH}")
    joblib.dump(scaler, SCALER_PATH)
    
    metadata = {
        'movie_ids': movie_ids_list,
        'genre_id_to_index': genre_id_to_index,
        'all_genre_ids': all_genre_ids,
        'n_neighbors': n_neighbors,
        'feature_shape': feature_matrix.shape
    }
    logger.info(f"Saving metadata to {METADATA_PATH}")
    joblib.dump(metadata, METADATA_PATH)
    
    logger.info("Training complete!")
    logger.info(f"Model trained on {len(movie_ids_list)} movies with {feature_matrix.shape[1]} features")


if __name__ == "__main__":
    train_knn_model()
