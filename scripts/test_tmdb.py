from backend.services.tmdb_service import fetch_popular_movies

movies = fetch_popular_movies(page=1)

print(f"Popular movies on page 1: {len(movies)} ")

print(movies)