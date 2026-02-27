from pydantic import BaseModel

class AddRatingRequest(BaseModel):
    """Request rating of movie."""
    tmdb_id: int
    score: int