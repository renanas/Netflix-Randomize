from fastapi import APIRouter, HTTPException, Depends
from typing import List
from backend.services.user_service import UserService
from backend.models.rating import (
    AddRatingRequest
)
from backend.utils.auth import verify_token

router = APIRouter()

user_service = None

def get_service():
    global user_service
    if user_service is None:
        user_service = UserService()
    return user_service


@router.post("/rating/add", status_code=201)
def add_movie_rating(
    request: AddRatingRequest,
    user_id: str = Depends(verify_token)
):
    """
    Adding a rating to a movie for the authenticated user.
    """
    try:
        service = get_service()
        service.add_rating(user_id, request.tmdb_id, request.link)
        return {"message": f"Fetched and saved {len(movies)} movies", "movies": movies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))