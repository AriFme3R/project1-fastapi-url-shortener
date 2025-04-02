from fastapi import HTTPException
from fastapi import status

from .crud import SHORTENED_URLS
from schemas.shortened_url import ShortenedUrl


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
