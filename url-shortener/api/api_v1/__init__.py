from fastapi import APIRouter

from .shortened_urls.views import router as shortened_urls_router

router = APIRouter(
    prefix="/v1",
)

router.include_router(shortened_urls_router)
