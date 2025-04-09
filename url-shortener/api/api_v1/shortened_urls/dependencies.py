import logging

from fastapi import (
    HTTPException,
    BackgroundTasks,
    Request,
)
from fastapi import status

from .crud import storage
from schemas.shortened_url import ShortenedUrl


logger = logging.getLogger(__name__)

UNSAFE_METHOD = frozenset(
    [
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    ]
)


def prefetch_shortened_url(
    slug: str,
) -> ShortenedUrl:
    url: ShortenedUrl | None = storage.get_by_slug(slug=slug)
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL {slug!r} not found",
    )


def save_storage_safe(
    request: Request,
    background_task: BackgroundTasks,
):
    # сначала код до входа внутрь view функции
    yield
    # код после покидания view функции
    if request.method in UNSAFE_METHOD:
        logger.info("Add background task to save storage")
        background_task.add_task(storage.save_state)
