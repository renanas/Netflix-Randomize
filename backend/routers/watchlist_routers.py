from fastapi import APIRouter, HTTPException, Depends
from typing import List
from backend.services.watchlist_service import WatchlistService
from backend.models.watchlist import (
    AddMovieRequest,
    WatchlistResponse,
    WatchlistDetailResponse,
    CheckMovieResponse,
    RemoveMovieResponse
)
from backend.utils.auth import verify_token

router = APIRouter()

watchlist_service = None

def get_service():
    global watchlist_service
    if watchlist_service is None:
        watchlist_service = WatchlistService()
    return watchlist_service


@router.post("/watchlist/add", status_code=201)
def add_movie_to_watchlist(
    request: AddMovieRequest,
    user_id: str = Depends(verify_token)
):
    """
    Add a movie to the authenticated user's watchlist.
    
    Request body:
    {
        "tmdb_id": 550
    }
    
    Returns 201 Created with the movie added.
    Returns 400 if movie already in watchlist.
    Returns 404 if movie doesn't exist in database.
    """
    try:
        service = get_service()
        result = service.add_movie(user_id, request.tmdb_id)
        return result
    except ValueError as e:
        error_msg = str(e)
        # Different error codes for different scenarios
        if "not found in database" in error_msg:
            raise HTTPException(status_code=404, detail=error_msg)
        elif "already in your watchlist" in error_msg:
            raise HTTPException(status_code=400, detail=error_msg)
        else:
            raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.delete("/watchlist/remove/{tmdb_id}", status_code=200)
def remove_movie_from_watchlist(
    tmdb_id: int,
    user_id: str = Depends(verify_token)
):
    """
    Remove a movie from the authenticated user's watchlist.
    
    Path parameter: tmdb_id (movie ID from TMDB)
    
    Returns 200 with confirmation.
    Returns 404 if movie not in watchlist.
    """
    try:
        service = get_service()
        result = service.remove_movie(user_id, tmdb_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/watchlist", response_model=WatchlistResponse)
def get_watchlist(
    user_id: str = Depends(verify_token)
):
    """
    Get all movies in the authenticated user's watchlist (IDs only).
    
    Returns:
    {
        "my_list": [550, 278, 680],
        "count": 3
    }
    """
    try:
        service = get_service()
        result = service.get_watchlist(user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/watchlist/detailed", response_model=WatchlistDetailResponse)
def get_watchlist_detailed(
    user_id: str = Depends(verify_token)
):
    """
    Get all movies in the authenticated user's watchlist with full details.
    
    Returns movie information including title, poster, release date, etc.
    {
        "my_list": [
            {
                "id": 550,
                "title": "Fight Club",
                "poster_path": "/a28h264t-jp2j6OMoVzsnGAB55Pp.jpg",
                "release_date": "1999-10-15",
                "overview": "...",
                "vote_average": 8.5
            }
        ],
        "count": 1
    }
    """
    try:
        service = get_service()
        result = service.get_watchlist_detailed(user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/watchlist/check/{tmdb_id}", status_code=200)
def check_movie_in_watchlist(
    tmdb_id: int,
    user_id: str = Depends(verify_token)
):
    """
    Check if a specific movie is in the authenticated user's watchlist.
    
    Path parameter: tmdb_id (movie ID from TMDB)
    
    Returns:
    {
        "tmdb_id": 550,
        "in_watchlist": true
    }
    """
    try:
        service = get_service()
        result = service.check_movie_in_watchlist(user_id, tmdb_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
