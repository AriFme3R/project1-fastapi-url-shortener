from fastapi import HTTPException
from fastapi import status

from .crud import MOVIES
from schemas.movie import Movie


def prefetch_movie(
    movie_id: int,
) -> Movie:
    movie_details: Movie | None = next(
        (movie for movie in MOVIES if movie.id == movie_id),
        None,
    )
    if movie_details:
        return movie_details
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie {movie_id!r} not found",
    )
