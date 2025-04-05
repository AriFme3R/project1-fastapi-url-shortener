from pydantic import AnyHttpUrl, BaseModel

from schemas.shortened_url import (
    ShortenedUrl,
    ShortenedUrlCreate,
    ShortenedUrlUpdate,
)


class ShortenedUrlsStorage(BaseModel):
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


storage = ShortenedUrlsStorage()

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
