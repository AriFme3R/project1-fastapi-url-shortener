from pydantic import AnyHttpUrl

from schemas.shortened_url import ShortenedUrl

SHORTENED_URLS = [
    ShortenedUrl(
        target_url=AnyHttpUrl("https://example.com"),
        slug="example",
    ),
    ShortenedUrl(
        target_url=AnyHttpUrl("https://google.com"),
        slug="search",
    ),
]
