from typing import Annotated

from fastapi import APIRouter, Depends, BackgroundTasks
from starlette import status

from api.api_v1.shortened_urls.crud import storage
from api.api_v1.shortened_urls.dependencies import (
    prefetch_shortened_url,
)
from schemas.shortened_url import (
    ShortenedUrl,
    ShortenedUrlUpdate,
    ShortenedUrlPartialUpdate,
    ShortenedUrlRead,
)

router = APIRouter(
    prefix="/{slug}",
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

ShortenedUrlBySlug = Annotated[
    ShortenedUrl,
    Depends(prefetch_shortened_url),
]


@router.get(
    "/",
    response_model=ShortenedUrlRead,
)
def read_shortened_url_details(
    url: ShortenedUrlBySlug,
) -> ShortenedUrl:
    return url


@router.put(
    "/",
    response_model=ShortenedUrlRead,
)
def update_shortened_url_details(
    url: ShortenedUrlBySlug,
    shortened_url_in: ShortenedUrlUpdate,
) -> ShortenedUrl:
    return storage.update(
        shortened_url=url,
        shortened_url_in=shortened_url_in,
    )


@router.patch(
    "/",
    response_model=ShortenedUrlRead,
)
def update_shortened_url_details_partial(
    url: ShortenedUrlBySlug,
    shortened_url_in: ShortenedUrlPartialUpdate,
) -> ShortenedUrl:
    return storage.update_partial(
        shortened_url=url,
        shortened_url_in=shortened_url_in,
    )


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_shortened_url(
    url: ShortenedUrlBySlug,
) -> None:
    storage.delete(shortened_url=url)
