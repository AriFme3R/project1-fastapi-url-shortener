from typing import Annotated

from annotated_types import Len

from fastapi import (
    Depends,
    APIRouter,
    status,
    Form,
)
from pydantic import AnyHttpUrl

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


@router.post(
    "/",
    response_model=ShortenedUrl,
    status_code=status.HTTP_201_CREATED,
)
def create_shortened_url(
    target_url: Annotated[AnyHttpUrl, Form()],
    slug: Annotated[
        str,
        Len(min_length=3, max_length=10),
        Form(),
    ],
) -> ShortenedUrl:
    return ShortenedUrl(
        target_url=target_url,
        slug=slug,
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
