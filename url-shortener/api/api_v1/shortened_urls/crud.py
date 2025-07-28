__all__ = ("storage",)

import logging

from pydantic import BaseModel
from redis import Redis

from core import config
from schemas.shortened_url import (
    ShortenedUrl,
    ShortenedUrlCreate,
    ShortenedUrlPartialUpdate,
    ShortenedUrlUpdate,
)

logger = logging.getLogger(__name__)

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_SHORTENED_URLS,
    decode_responses=True,
)


class ShortenedUrlBaseError(Exception):
    """
    Base exception for shortened url CRUD actions.
    """


class ShortenedUrlAlreadyExists(ShortenedUrlBaseError):
    """
    Raise on shortened url creation if such slug already exists.
    """


class ShortenedUrlsStorage(BaseModel):

    def save_shortened_url(self, shortened_url: ShortenedUrl) -> None:
        redis.hset(
            name=config.REDIS_SHORTENED_URLS_HASH_NAME,
            key=shortened_url.slug,
            value=shortened_url.model_dump_json(),
        )

    def get(self) -> list[ShortenedUrl]:
        data = redis.hvals(
            name=config.REDIS_SHORTENED_URLS_HASH_NAME,
        )
        return [ShortenedUrl.model_validate_json(value) for value in data]

    def get_by_slug(self, slug: str) -> ShortenedUrl | None:
        data = redis.hget(
            name=config.REDIS_SHORTENED_URLS_HASH_NAME,
            key=slug,
        )
        if data:
            return ShortenedUrl.model_validate_json(data)
        return None

    def exists(self, slug: str) -> bool:
        return bool(
            redis.hexists(
                name=config.REDIS_SHORTENED_URLS_HASH_NAME,
                key=slug,
            )
        )

    def create(self, shortened_url_in: ShortenedUrlCreate) -> ShortenedUrl:
        shortened_url = ShortenedUrl(
            **shortened_url_in.model_dump(),
        )
        self.save_shortened_url(shortened_url)
        logger.info("Created shortened url %s", shortened_url)
        return shortened_url

    def create_or_raise_if_exists(
        self, shortened_url_in: ShortenedUrlCreate
    ) -> ShortenedUrl:
        if not self.exists(shortened_url_in.slug):
            return self.create(shortened_url_in)

        raise ShortenedUrlAlreadyExists(shortened_url_in.slug)

    def delete_by_slug(self, slug: str) -> None:
        redis.hdel(
            config.REDIS_SHORTENED_URLS_HASH_NAME,
            slug,
        )

    def delete(self, shortened_url: ShortenedUrl) -> None:
        self.delete_by_slug(slug=shortened_url.slug)

    def update(
        self,
        shortened_url: ShortenedUrl,
        shortened_url_in: ShortenedUrlUpdate,
    ) -> ShortenedUrl:
        for field_name, value in shortened_url_in:
            setattr(shortened_url, field_name, value)
        self.save_shortened_url(shortened_url)
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
        self.save_shortened_url(shortened_url)
        return shortened_url


storage = ShortenedUrlsStorage()
