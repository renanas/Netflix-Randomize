from backend.database.mongo_connection import db

collection = db["movies"]

def save_movie(movie_data):
    """
    Save movie data to the database. If it already exists (by TMDb id), ignore.
    """
    movie_id = movie_data.get("id")
    if not movie_id:
        raise ValueError("movie_data need contains 'id' on TMDB")

    # Evita duplicados
    existing = collection.find_one({"id": movie_id})
    if existing:
        return existing["_id"]

    result = collection.insert_one(movie_data)
    return result.inserted_id


def save_many_movies(movies_list):
    """
    Save many movies to the database. Ignoring duplicates.
    """
    saved_ids = []
    for movie in movies_list:
        saved_ids.append(save_movie(movie))
    return saved_ids


def get_all_movies(limit=50):
    """
    Return movies stored.
    """
    return list(collection.find().limit(limit))


def get_movie_by_tmdb_id(movie_id):
    """
    Get movie by ID of TMDb.
    """
    return collection.find_one({"id": movie_id})
