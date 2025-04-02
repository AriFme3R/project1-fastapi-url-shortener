from typing import Annotated

from fastapi import Depends, APIRouter

from .dependencies import prefetch_movie
from .crud import MOVIES
from schemas.movie import Movie

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)


@router.get(
    "/",
    response_model=list[Movie],
)
def read_movies_list():
    return MOVIES


@router.get(
    "/{movie_id}/",
    response_model=Movie,
)
def read_movie_details(
    movie_details: Annotated[
        Movie,
        Depends(prefetch_movie),
    ],
) -> Movie:
    return movie_details
