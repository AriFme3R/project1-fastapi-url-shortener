from fastapi import (
    APIRouter,
    status,
)

from schemas.shortened_url import (
    ShortenedUrl,
    ShortenedUrlCreate,
)

from api.api_v1.shortened_urls.crud import storage

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
