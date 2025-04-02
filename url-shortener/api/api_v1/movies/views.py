from random import randint
from typing import Annotated
from annotated_types import Len

from fastapi import (
    Depends,
    APIRouter,
    status,
    Form,
)

from .dependencies import prefetch_movie
from .crud import MOVIES
from schemas.movie import Movie, MovieCreate

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


@router.post(
    "/",
    response_model=Movie,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(
    movie_create: MovieCreate,
):
    return Movie(
        **movie_create.model_dump(),
    )


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
