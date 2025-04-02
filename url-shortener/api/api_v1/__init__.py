from fastapi import APIRouter

from .shortened_urls.views import router as shortened_urls_router
from .movies.views import router as movies_router

router = APIRouter(
    prefix="/v1",
)

router.include_router(shortened_urls_router)
router.include_router(movies_router)
