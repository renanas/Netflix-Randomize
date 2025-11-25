import os 
import requests
from dotenv import load_dotenv

load_dotenv()
TMDB_BEARER_TOKEN = os.getenv("TMDB_BEARER_TOKEN")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

def fetch_popular_movies(page: int = 1):
    url = f"{TMDB_BASE_URL}/movie/popular"
    
    headers = {
        "Authorization": f"Bearer {TMDB_BEARER_TOKEN}",
        "Content-Type": "application/json;charset=utf-8"
    }

    params = {
        "language": "en-US",
        "page": page
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"TMDB API request failed with status code {response.status_code}")
    
    return response.json()

def fetch_movie_details(movie_id: int):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}"

    headers = {
        "Authorization": f"Bearer {TMDB_BEARER_TOKEN}",
        "Content-Type": "application/json;charset=utf-8"
    }

    params = {
        "language": "pt-BR",
        "append_to_response": "videos,credits"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"TMDB API request failed with status code {response.status_code}")
    
    return response.json()