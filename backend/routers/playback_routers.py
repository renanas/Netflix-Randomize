from fastapi import APIRouter, HTTPException, Depends
from backend.services.playback_service import PlaybackService
from backend.models.user import PlayMovieRequest, PauseMovieRequest
from backend.utils.auth import verify_token

router = APIRouter()

playback_service = None

def get_service():
    global playback_service
    if playback_service is None:
        playback_service = PlaybackService()
    return playback_service


@router.post("/playback/play", status_code=200)
def play_movie(
    request: PlayMovieRequest,
    user_id: str = Depends(verify_token)
):
    """
    Start playing a movie - adds it to user's viewing history.
    """
    try:
        print(f"Playing movie {request.tmdb_id} for user {user_id}")
        service = get_service()
        result = service.play_movie(user_id, request.tmdb_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/playback/pause", status_code=200)
def pause_movie(
    request: PauseMovieRequest,
    user_id: str = Depends(verify_token)
):
    """
    Pause a movie - removes from viewing history and saves playback position.
    Requires the number of seconds where the user paused.
    """
    try:
        print(f"Pausing movie {request.tmdb_id} at {request.seconds} seconds for user {user_id}")
        service = get_service()
        result = service.pause_movie(user_id, request.tmdb_id, request.seconds)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
