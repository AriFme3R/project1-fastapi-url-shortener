from unittest import TestCase

from schemas.shortened_url import (
    ShortenedUrl,
    ShortenedUrlCreate,
)


class ShortenedUrlCreateTestCase(TestCase):
    def test_shortened_url_can_be_created_from_create_schema(self) -> None:
        shortened_url_in = ShortenedUrlCreate(
            slug="Some-slug",
            description="some-description",
            target_url="https://example.com",
        )
        shortened_url = ShortenedUrl(
            **shortened_url_in.model_dump(),
        )

        self.assertEqual(shortened_url_in.slug, shortened_url.slug)
        self.assertEqual(shortened_url_in.target_url, shortened_url.target_url)
        self.assertEqual(shortened_url_in.description, shortened_url.description)
