from typing import Annotated

from fastapi import (
    Depends,
    APIRouter,
    status,
)

from schemas.shortened_url import (
    ShortenedUrl,
    ShortenedUrlCreate,
)

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


@router.post(
    "/",
    response_model=ShortenedUrlCreate,
    status_code=status.HTTP_201_CREATED,
)
def create_shortened_url(
    shortened_url_create: ShortenedUrlCreate,
):
    return ShortenedUrl(
        **shortened_url_create.model_dump(),
    )


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
