from typing import Annotated

from fastapi import Depends, APIRouter
from starlette.responses import RedirectResponse

from .api_v1.shortened_urls.dependencies import prefetch_shortened_url
from schemas.shortened_url import ShortenedUrl


router = APIRouter(
    prefix="/r",
    tags=["Redirect"],
)


@router.get("/{slug}")
@router.get("/{slug}/")
def redirect_shortened_url(
    url: Annotated[
        ShortenedUrl,
        Depends(prefetch_shortened_url),
    ],
) -> RedirectResponse:
    return RedirectResponse(
        url=str(url.target_url),
    )
