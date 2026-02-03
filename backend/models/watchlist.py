from pydantic import BaseModel
from typing import List, Optional


class AddMovieRequest(BaseModel):
    """Request model for adding a movie to watchlist."""
    tmdb_id: int


class WatchlistResponse(BaseModel):
    """Response model for watchlist with movie IDs only."""
    my_list: List[int]
    count: int


class MovieDetail(BaseModel):
    """Detailed movie information for watchlist responses."""
    id: int
    title: str
    poster_path: Optional[str] = None
    release_date: Optional[str] = None
    overview: Optional[str] = None
    vote_average: Optional[float] = None


class WatchlistDetailResponse(BaseModel):
    """Response model for watchlist with full movie details."""
    my_list: List[dict]
    count: int


class CheckMovieResponse(BaseModel):
    """Response model for checking if movie is in watchlist."""
    tmdb_id: int
    in_watchlist: bool


class RemoveMovieResponse(BaseModel):
    """Response model for removing a movie from watchlist."""
    message: str
    tmdb_id: int
    my_list_count: int
