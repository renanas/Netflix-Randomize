from fastapi import APIRouter, HTTPException, Depends
from typing import List
from backend.services.rating_service import RatingService
from backend.models.rating import (
    AddRatingRequest
)
from backend.utils.auth import verify_token

router = APIRouter()

rating_service = None

def get_service():
    global rating_service
    if rating_service is None:
        rating_service = RatingService()
    return rating_service


@router.post("/rating/add", status_code=201)
def add_movie_rating(
    request: AddRatingRequest,
    user_id: str = Depends(verify_token)
):
    """
    Adding a rating to a movie for the authenticated user.
    """
    try:
        print(f"Received rating request: {request} for user_id: {user_id}")
        rating_service = get_service()
        rating_service.add_rating(user_id, request.tmdb_id, request.score)
        return {"message": f"Rating added for movie {request.tmdb_id} by user {user_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))