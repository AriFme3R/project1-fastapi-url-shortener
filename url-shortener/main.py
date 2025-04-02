from typing import Annotated

from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    status,
    Depends,
)

from api import router as api_router
from api.redirect_views import router as redirect_views

from schemas.movie import Movie

app = FastAPI(
    title="URL Shortener",
)

app.include_router(redirect_views)
app.include_router(api_router)


@app.get("/")
def read_root(
    request: Request,
    name: str = "World",
):
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    return {
        "Message": f"Hello, {name}!",
        "docs": str(docs_url),
    }


MOVIES = [
    Movie(
        id=1,
        title="Криминальное чтиво",
        description="Двое бандитов Винсент Вега и Джулс Винфилд ведут философские беседы в перерывах между разборками и решением проблем с должниками криминального босса Марселласа Уоллеса.",
        year=1995,
        duration=154,
    ),
    Movie(
        id=2,
        title="От заката до рассвета",
        description="Спасаясь от полиции после ограбления банка, два брата-преступника берут в заложники священника с двумя детьми и бегут в Мексику. Там они должны дождаться подельника, а для этого всей компании нужно переждать ночь в баре дальнобойщиков.",
        year=1995,
        duration=108,
    ),
    Movie(
        id=3,
        title="Бесславные ублюдки",
        description="Вторая мировая война. В оккупированной немцами Франции группа американских солдат-евреев наводит страх на нацистов, жестоко убивая и скальпируя солдат.",
        year=2009,
        duration=153,
    ),
]


@app.get(
    "/movies/",
    response_model=list[Movie],
)
def read_movies_list():
    return MOVIES


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


@app.get(
    "/movies/{movie_id}/",
    response_model=Movie,
)
def read_movie_details(
    movie_details: Annotated[
        Movie,
        Depends(prefetch_movie),
    ],
) -> Movie:
    return movie_details
