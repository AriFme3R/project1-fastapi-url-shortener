from typing import Annotated

from annotated_types import Len, MaxLen
from pydantic import AnyHttpUrl, BaseModel

DescriptionString = Annotated[
    str,
    MaxLen(200),
]


class ShortenedUrlBase(BaseModel):
    target_url: AnyHttpUrl
    description: DescriptionString


class ShortenedUrlCreate(ShortenedUrlBase):
    """
    Модель для создания сокращённой ссылки
    """

    slug: Annotated[
        str,
        Len(min_length=3, max_length=10),
    ]
    description: DescriptionString = ""


class ShortenedUrlUpdate(ShortenedUrlBase):
    """
    Модель для обновления информации о сокращённой ссылки
    """


class ShortenedUrlPartialUpdate(BaseModel):
    """
    Модель для частичного обновления информации
    о сокращённой ссылки
    """

    target_url: AnyHttpUrl | None = None
    description: DescriptionString | None = None


class ShortenedUrlRead(ShortenedUrlBase):
    """
    Модель для чтения данных по короткой ссылке
    """

    slug: str
    description: str


class ShortenedUrl(ShortenedUrlBase):
    """
    Модель сокращённой ссылки
    """

    slug: str
    description: str
    visits: int = 42
