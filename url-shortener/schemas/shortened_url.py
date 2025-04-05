from typing import Annotated

from pydantic import BaseModel, AnyHttpUrl
from annotated_types import Len, MaxLen


DescriptionString = Annotated[
    str,
    MaxLen(200),
]


class ShortenedUrlBase(BaseModel):
    target_url: AnyHttpUrl
    description: DescriptionString = ""


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

    description: DescriptionString


class ShortenedUrlPartialUpdate(ShortenedUrlBase):
    """
    Модель для частичного обновления информации
    о сокращённой ссылки
    """

    target_url: AnyHttpUrl | None = None
    description: DescriptionString | None = None


class ShortenedUrl(ShortenedUrlBase):
    """
    Модель сокращённой ссылки
    """

    slug: str
