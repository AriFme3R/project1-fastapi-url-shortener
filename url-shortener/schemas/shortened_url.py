from typing import Annotated

from pydantic import BaseModel, AnyHttpUrl
from annotated_types import Len, MaxLen


class ShortenedUrlBase(BaseModel):
    target_url: AnyHttpUrl
    description: Annotated[
        str,
        MaxLen(200),
    ] = ""


class ShortenedUrlCreate(ShortenedUrlBase):
    """
    Модель для создания сокращённой ссылки
    """

    slug: Annotated[
        str,
        Len(min_length=3, max_length=10),
    ]


class ShortenedUrlUpdate(ShortenedUrlBase):
    """
    Модель для обновления информации о сокращённой ссылки
    """


class ShortenedUrl(ShortenedUrlBase):
    """
    Модель сокращённой ссылки
    """

    slug: str
