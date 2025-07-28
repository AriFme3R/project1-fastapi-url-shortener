from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from api.api_v1.shortened_urls.crud import ShortenedUrlAlreadyExists, storage
from api.api_v1.shortened_urls.dependencies import (
    api_token_or_user_basic_auth_required_for_unsafe_methods,
)
from schemas.shortened_url import (
    ShortenedUrl,
    ShortenedUrlCreate,
    ShortenedUrlRead,
)

router = APIRouter(
    prefix="/short_urls",
    tags=["Shortened_urls"],
    dependencies=[
        Depends(api_token_or_user_basic_auth_required_for_unsafe_methods),
    ],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized. Only for unsafe methods!",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid API token or basic auth.",
                    }
                }
            },
        },
    },
)


@router.get(
    "/",
    response_model=list[ShortenedUrlRead],
)
def read_short_urls_list() -> list[ShortenedUrl]:
    return storage.get()


@router.post(
    "/",
    response_model=ShortenedUrlRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "It is not possible to overwrite an existing record.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Shortened URL with slug='name' already exists",
                    }
                }
            },
        },
    },
)
def create_shortened_url(
    shortened_url_create: ShortenedUrlCreate,
) -> ShortenedUrl:
    try:
        return storage.create_or_raise_if_exists(shortened_url_create)
    except ShortenedUrlAlreadyExists:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Shortened URL with slug={shortened_url_create.slug!r} already exists",
        )
