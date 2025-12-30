from fastapi import FastAPI
from backend.services.tmdb_service import fetch_popular_movies, fetch_movie_details

app = FastAPI(
    title="Netflix Clone API",
    version="1.0.0",
)

@app.get("/")
def root():
    return {"message": "Welcome to the Netflix Clone API!"}

@app.get("/fetch-popular")
def get_popular_movies(page: int = 1):
    """
    Fetch popular movies from TMDB and save them to the database.
    """
    try:
        movies = fetch_popular_movies(page)
        return {"message": f"Fetched and saved {len(movies)} movies", "movies": movies}
    except Exception as e:
        return {"error": str(e)}

@app.get("/movie/{movie_id}")
def get_movie_details(movie_id: int):
    """
    Fetch movie details from TMDB and save to the database.
    """
    try:
        details = fetch_movie_details(movie_id)
        return details
    except Exception as e:
        return {"error": str(e)}