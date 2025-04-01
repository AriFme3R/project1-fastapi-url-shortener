from typing import Annotated

from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    status,
    Depends,
)
from fastapi.responses import (
    RedirectResponse,
)

from schemas.shortened_url import ShortenedUrl
from schemas.movie import Movie

app = FastAPI(
    title="URL Shortener",
)


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


SHORTENED_URLS = [
    ShortenedUrl(
        target_url="https://example.com",
        slug="example",
    ),
    ShortenedUrl(
        target_url="https://google.com",
        slug="search",
    ),
]


@app.get(
    "/short_urls/",
    response_model=list[ShortenedUrl],
)
def read_short_urls_list():
    return SHORTENED_URLS


def prefetch_shortened_url(
    slug: str,
) -> ShortenedUrl:
    url: ShortenedUrl | None = next(
        (url for url in SHORTENED_URLS if url.slug == slug),
        None,
    )
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL {slug!r} not found",
    )


@app.get("/r/{slug}")
@app.get("/r/{slug}/")
def redirect_shortened_url(
    url: Annotated[
        ShortenedUrl,
        Depends(prefetch_shortened_url),
    ],
):
    return RedirectResponse(
        url=url.target_url,
    )


@app.get(
    "/short-urls/{slug}/",
    response_model=ShortenedUrl,
)
def read_shortened_url_details(
    url: Annotated[
        ShortenedUrl,
        Depends(prefetch_shortened_url),
    ],
) -> ShortenedUrl:
    return url


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
