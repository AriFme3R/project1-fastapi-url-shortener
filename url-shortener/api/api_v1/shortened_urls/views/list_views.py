from fastapi import (
    APIRouter,
    status,
    Depends,
)

from api.api_v1.shortened_urls.dependencies import (
    save_storage_safe,
    api_token_or_user_basic_auth_required_for_unsafe_methods,
)
from schemas.shortened_url import (
    ShortenedUrl,
    ShortenedUrlCreate,
    ShortenedUrlRead,
)

from api.api_v1.shortened_urls.crud import storage

router = APIRouter(
    prefix="/short_urls",
    tags=["Shortened_urls"],
    dependencies=[
        Depends(save_storage_safe),
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
)
def create_shortened_url(
    shortened_url_create: ShortenedUrlCreate,
) -> ShortenedUrl:
    return storage.create(shortened_url_create)
