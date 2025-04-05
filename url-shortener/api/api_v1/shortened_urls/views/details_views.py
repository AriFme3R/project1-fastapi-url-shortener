from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from api.api_v1.shortened_urls.crud import storage
from api.api_v1.shortened_urls.dependencies import prefetch_shortened_url
from schemas.shortened_url import ShortenedUrl

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


@router.get(
    "/",
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
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_shortened_url(
    url: Annotated[
        ShortenedUrl,
        Depends(prefetch_shortened_url),
    ],
) -> None:
    storage.delete(shortened_url=url)
