from fastapi import HTTPException
from fastapi import status

from .crud import storage
from schemas.movie import Movie


def prefetch_movie(
    slug: str,
) -> Movie:
    movie_details: Movie | None = storage.get_by_slug(slug=slug)
    if movie_details:
        return movie_details
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie {slug!r} not found",
    )
