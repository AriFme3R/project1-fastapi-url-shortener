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
