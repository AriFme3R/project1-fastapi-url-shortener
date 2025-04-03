from pydantic import AnyHttpUrl, BaseModel

from schemas.shortened_url import (
    ShortenedUrl,
    ShortenedUrlCreate,
)


class ShortenedUrlsShorage(BaseModel):
    slug_to_shortened_url: dict[str, ShortenedUrl] = {}

    def get(self) -> list[ShortenedUrl]:
        return list(self.slug_to_shortened_url.values())

    def get_by_slug(self, slug: str) -> ShortenedUrl | None:
        return self.slug_to_shortened_url.get(slug)

    def create(self, shortened_url: ShortenedUrlCreate) -> ShortenedUrl:
        shortened_url = ShortenedUrl(
            **shortened_url.model_dump(),
        )
        self.slug_to_shortened_url[shortened_url.slug] = shortened_url
        return shortened_url


storage = ShortenedUrlsShorage()

storage.create(
    ShortenedUrlCreate(
        target_url=AnyHttpUrl("https://example.com"),
        slug="example",
    ),
)

storage.create(
    ShortenedUrlCreate(
        target_url=AnyHttpUrl("https://google.com"),
        slug="search",
    ),
)
