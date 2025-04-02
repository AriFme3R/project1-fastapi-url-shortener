from typing import Annotated

from fastapi import Depends, APIRouter

from schemas.shortened_url import ShortenedUrl

from .crud import SHORTENED_URLS
from .dependencies import (
    prefetch_shortened_url,
)


router = APIRouter(
    prefix="/short_urls",
    tags=["Shortened_urls"],
)


@router.get(
    "/",
    response_model=list[ShortenedUrl],
)
def read_short_urls_list():
    return SHORTENED_URLS


@router.get(
    "/{slug}/",
    response_model=ShortenedUrl,
)
def read_shortened_url_details(
    url: Annotated[
        ShortenedUrl,
        Depends(prefetch_shortened_url),
    ],
) -> ShortenedUrl:
    return url
