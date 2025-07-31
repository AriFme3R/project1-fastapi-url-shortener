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

    def test_shortened_url_create_accepts_different_urls(self) -> None:
        urls = [
            "http://example.com",
            "https://example.com",
            # "rtmp://video.example.com",
            # "rtmps://video.example.com",
            "http://abc.example.com",
            "https://www.example.com/foobar/",
        ]
        for url in urls:
            with self.subTest(url=url, msg=f"test-url-{url}"):
                shortened_url_create = ShortenedUrlCreate(
                    slug="some-slug",
                    description="some-description",
                    target_url=url,
                )

                self.assertEqual(
                    url.rstrip("/"),
                    shortened_url_create.model_dump(mode="json")["target_url"].rstrip(
                        "/",
                    ),
                )
