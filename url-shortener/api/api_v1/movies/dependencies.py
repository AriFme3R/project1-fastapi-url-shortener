from fastapi import HTTPException
from fastapi import status

from .crud import MOVIES
from schemas.movie import Movie


def prefetch_movie(
    slug: str,
) -> Movie:
    movie_details: Movie | None = next(
        (movie for movie in MOVIES if movie.slug == slug),
        None,
    )
    if movie_details:
        return movie_details
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie {slug!r} not found",
    )
