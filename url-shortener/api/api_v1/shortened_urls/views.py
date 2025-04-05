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

from .crud import storage
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
def read_short_urls_list() -> list[ShortenedUrl]:
    return storage.get()


@router.post(
    "/",
    response_model=ShortenedUrlCreate,
    status_code=status.HTTP_201_CREATED,
)
def create_shortened_url(
    shortened_url_create: ShortenedUrlCreate,
) -> ShortenedUrl:
    return storage.create(shortened_url_create)


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


@router.delete(
    "/{slug}/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Shortened URL not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "URL 'slug' not found",
                    },
                },
            },
        },
    },
)
def delete_shortened_url(
    url: Annotated[
        ShortenedUrl,
        Depends(prefetch_shortened_url),
    ],
) -> None:
    storage.delete(shortened_url=url)
