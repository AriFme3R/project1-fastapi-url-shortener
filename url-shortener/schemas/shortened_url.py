from typing import Annotated

from pydantic import BaseModel, AnyHttpUrl
from annotated_types import Len


class ShortenedUrlBase(BaseModel):
    target_url: AnyHttpUrl
    slug: str


class ShortenedUrlCreate(ShortenedUrlBase):
    """
    Модель для создания сокращённой ссылки
    """

    slug: Annotated[
        str,
        Len(min_length=3, max_length=10),
    ]


class ShortenedUrl(ShortenedUrlBase):
    """
    Модель сокращённой ссылки
    """
