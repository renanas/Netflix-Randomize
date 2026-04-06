from fastapi import APIRouter, HTTPException, Depends
from backend.utils.auth import verify_token
from backend.services.recommendation_service import RecommendationService
import random

router = APIRouter()

# Create a new service instance per request. Keeps behavior stateless for tests.

def get_recommendation_service():
    return RecommendationService()


@router.get("/recommendationMovie", response_model=list)
def recommendation_movie(user_id: str = Depends(verify_token)):
    """Recommend movies for the authenticated user."""
    try:
        service = get_recommendation_service()
        movies = service.recommend_movies_for_user(user_id, min_recommendations=3)
        return movies
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print('recommendation internal error', repr(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recommendationMovie/refresh", response_model=list)
def recommendation_movie_refresh(user_id: str = Depends(verify_token)):
    """Force rebuild recommendation for the authenticated user."""
    try:
        service = get_recommendation_service()
        movies = service.recommend_movies_for_user(user_id, min_recommendations=3, force_refresh=True)
        return movies
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print('recommendation refresh internal error', repr(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/randomMovie", response_model=dict)
def random_movie(user_id: str = Depends(verify_token)):
    """Get a random movie from user's recommendations."""
    try:
        service = get_recommendation_service()
        # Pega lista de filmes recomendados
        movies = service.recommend_movies_for_user(user_id, min_recommendations=5)
        
        if not movies:
            raise HTTPException(status_code=404, detail="No recommendations available for this user")
        
        # Seleciona um aleatoriamente
        random_movie = random.choice(movies)
        return random_movie
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print('random movie internal error', repr(e))
        raise HTTPException(status_code=500, detail=str(e))
