import sys
import os
import types
# Ensure project root is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fastapi.testclient import TestClient
from backend.utils.auth import create_access_token
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import joblib

# Fake user repository to avoid DB dependency
fake_user_repo = types.ModuleType('backend.repository.user_repository')

class FakeUserRepo:
    def get_user_by_id(self, user_id):
        if user_id != 'user123':
            return None
        return {
            '_id': 'user123',
            'profile': {
                'preferences': {
                    'favorite_genres': [18, 28, 12]
                }
            },
            'user_behavior': {
                'viewing_history': [
                    {'movie_id': 27205, 'watched_at': '2026-03-09T20:00:00'}
                ],
                'ratings': {
                    '27205': 1,
                    '118340': 1
                },
                'ignored_movies': []
            }
        }

fake_user_repo.UserRepository = FakeUserRepo
sys.modules['backend.repository.user_repository'] = fake_user_repo

# Fake movie repository to return sample movies
fake_movie_repo = types.ModuleType('backend.repository.movie_repository')

class FakeMovieRepo:
    def find_movies(self, query={}, limit=50):
        all_movies = [
            {'id': 27205, 'title': 'Watched Movie', 'genre_ids': [18]},
            {'id': 118340, 'title': 'Rated Movie', 'genre_ids': [28]},
            {'id': 12345, 'title': 'Action 1', 'genre_ids': [18]},
            {'id': 67890, 'title': 'Action 2', 'genre_ids': [28]},
            {'id': 55555, 'title': 'Drama 1', 'genre_ids': [12]},
            {'id': 99999, 'title': 'Other', 'genre_ids': [35]}
        ]

        if query:
            # Handle id filter
            if 'id' in query and isinstance(query['id'], dict) and '$in' in query['id']:
                id_list = query['id']['$in']
                all_movies = [m for m in all_movies if m.get('id') in id_list]
            # Handle genre filter
            elif 'genre_ids' in query:
                all_movies = [m for m in all_movies if set(m.get('genre_ids', [])) & set(query['genre_ids']['$in'])]
        
        return all_movies[:limit]

fake_movie_repo.MovieRepository = FakeMovieRepo
sys.modules['backend.repository.movie_repository'] = fake_movie_repo

fake_rec_repo = types.ModuleType('backend.repository.recommendation_repository')
class FakeRecommendationRepo:
    def __init__(self):
        self.storage = {}

    def upsert_recommendations(self, user_id, movie_ids):
        self.storage[user_id] = list(movie_ids)

    def get_recommendations(self, user_id):
        return self.storage.get(user_id)

    def delete_recommendations(self, user_id):
        self.storage.pop(user_id, None)

fake_rec_repo.RecommendationRepository = FakeRecommendationRepo
sys.modules['backend.repository.recommendation_repository'] = fake_rec_repo

# Create a fake KNN model and scaler for testing
def create_fake_knn_model():
    """Create fake KNN model with test movie IDs."""
    # Movie IDs from test movies
    test_movie_ids = [27205, 118340, 12345, 67890, 55555, 99999]
    n_movies = len(test_movie_ids)
    
    # Create fake feature vectors (random vectors for similarity testing)
    np.random.seed(42)
    X_fake = np.random.randn(n_movies, 10)  # 10-dimensional feature vectors
    
    # Fit scaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_fake)
    
    # Train KNN model
    knn = NearestNeighbors(n_neighbors=min(5, n_movies), metric='cosine')
    knn.fit(X_scaled)
    
    # Create metadata with movie IDs and genre mapping
    metadata = {
        'movie_ids': test_movie_ids,
        'genre_id_to_index': {18: 0, 28: 1, 12: 2, 35: 3}
    }
    
    return knn, scaler, metadata

# Patch recommendation_system.recommend module
fake_recommend = types.ModuleType('recommendation_system.recommend')

_fake_knn, _fake_scaler, _fake_metadata = create_fake_knn_model()

def fake_load_model():
    global _fake_knn, _fake_scaler, _fake_metadata
    return _fake_knn, _fake_scaler, _fake_metadata

def fake_recommend_similar_movies_with_data(reference_movies, exclude_ids=None, n_recommendations=20, return_distances=False):
    """Fake recommendation function that returns different movies from the reference ones."""
    if exclude_ids is None:
        exclude_ids = set()
    
    # All available test movies
    all_available = [
        {'id': 27205, 'title': 'Watched Movie', 'genre_ids': [18]},
        {'id': 118340, 'title': 'Rated Movie', 'genre_ids': [28]},
        {'id': 12345, 'title': 'Action 1', 'genre_ids': [18]},
        {'id': 67890, 'title': 'Action 2', 'genre_ids': [28]},
        {'id': 55555, 'title': 'Drama 1', 'genre_ids': [12]},
        {'id': 99999, 'title': 'Other', 'genre_ids': [35]}
    ]
    
    # Get watched movie ids from reference movies
    watched_ids = {m['id'] for m in reference_movies}
    
    # Recommend movies that are not watched and not excluded
    recommendations = []
    for movie in all_available:
        mid = movie['id']
        if mid not in watched_ids and mid not in exclude_ids:
            recommendations.append(mid if not return_distances else (mid, 0.5))
            if len(recommendations) >= n_recommendations:
                break
    
    return recommendations

fake_recommend.load_model = fake_load_model
fake_recommend.build_movie_feature_vector = lambda movie, metadata: np.array([
    *[1 if gid in movie.get('genre_ids', []) else 0 for gid in [18, 28, 12, 35]],
    *np.zeros(6)  # Padding to match 10 features
])
fake_recommend.recommend_similar_movies_with_data = fake_recommend_similar_movies_with_data

sys.modules['recommendation_system.recommend'] = fake_recommend

import backend.routers.recommendation_routers as recommendation_routers
from fastapi import FastAPI

app = FastAPI()
app.include_router(recommendation_routers.router, prefix="")
client = TestClient(app)


def test_recommendation_movie_returns_at_least_3():
    # Reassert stubs in case another test module replaced sys.modules
    sys.modules['backend.repository.user_repository'] = fake_user_repo
    sys.modules['backend.repository.movie_repository'] = fake_movie_repo
    sys.modules['backend.repository.recommendation_repository'] = fake_rec_repo

    # Reset cached service in router to ensure it rebuilds with correct dependencies
    import backend.routers.recommendation_routers as rec_mod
    rec_mod.recommendation_service = None

    token = create_access_token({'sub': 'user123'})
    resp = client.get('/recommendationMovie', headers={'Authorization': f'Bearer {token}'})
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 3
    ids = {m['id'] for m in data}
    assert 27205 not in ids
    assert 118340 not in ids


def test_recommendation_movie_refresh():
    sys.modules['backend.repository.user_repository'] = fake_user_repo
    sys.modules['backend.repository.movie_repository'] = fake_movie_repo
    sys.modules['backend.repository.recommendation_repository'] = fake_rec_repo

    import backend.routers.recommendation_routers as rec_mod
    rec_mod.recommendation_service = None

    token = create_access_token({'sub': 'user123'})
    resp = client.post('/recommendationMovie/refresh', headers={'Authorization': f'Bearer {token}'})
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 3

