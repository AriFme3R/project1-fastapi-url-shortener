import logging

from pydantic import BaseModel, ValidationError
from redis import Redis

from core import config
from core.config import SHORTENED_URLS_STORAGE_FILEPATH
from schemas.shortened_url import (
    ShortenedUrl,
    ShortenedUrlCreate,
    ShortenedUrlUpdate,
    ShortenedUrlPartialUpdate,
)

logger = logging.getLogger(__name__)

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_SHORTENED_URLS,
    decode_responses=True,
)


class ShortenedUrlsStorage(BaseModel):
    slug_to_shortened_url: dict[str, ShortenedUrl] = {}

    def save_state(self) -> None:
        SHORTENED_URLS_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=2))
        logger.info("Saved shortened urls storage file.")

    @classmethod
    def from_state(cls):
        if not SHORTENED_URLS_STORAGE_FILEPATH.exists():
            logger.info("Shortened urls storage file doesn't exist.")
            return ShortenedUrlsStorage()
        return cls.model_validate_json(SHORTENED_URLS_STORAGE_FILEPATH.read_text())

    def init_storage_from_state(self) -> None:
        try:
            data = ShortenedUrlsStorage.from_state()
        except ValidationError:
            self.save_state()
            logger.warning("Rewritten storage file.")
            return

        self.slug_to_shortened_url.update(
            data.slug_to_shortened_url,
        )
        logger.warning("Recovered data from storage file.")

    def get(self) -> list[ShortenedUrl]:
        return list(self.slug_to_shortened_url.values())

    def get_by_slug(self, slug: str) -> ShortenedUrl | None:
        return self.slug_to_shortened_url.get(slug)

    def create(self, shortened_url: ShortenedUrlCreate) -> ShortenedUrl:
        shortened_url = ShortenedUrl(
            **shortened_url.model_dump(),
        )
        redis.hset(
            name=config.REDIS_SHORTENED_URLS_HASH_NAME,
            key=shortened_url.slug,
            value=shortened_url.model_dump_json(),
        )
        logger.info("Created shortened url %s", shortened_url)
        return shortened_url

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_shortened_url.pop(slug, None)

    def delete(self, shortened_url: ShortenedUrl) -> None:
        self.delete_by_slug(slug=shortened_url.slug)

    def update(
        self,
        shortened_url: ShortenedUrl,
        shortened_url_in: ShortenedUrlUpdate,
    ) -> ShortenedUrl:
        for field_name, value in shortened_url_in:
            setattr(shortened_url, field_name, value)
        return shortened_url

    def update_partial(
        self,
        shortened_url: ShortenedUrl,
        shortened_url_in: ShortenedUrlPartialUpdate,
    ) -> ShortenedUrl:
        for field_name, value in shortened_url_in.model_dump(
            exclude_unset=True
        ).items():
            setattr(shortened_url, field_name, value)
        return shortened_url


storage = ShortenedUrlsStorage()
