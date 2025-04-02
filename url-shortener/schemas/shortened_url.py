from pydantic import BaseModel, AnyHttpUrl


class ShortenedUrlBase(BaseModel):
    target_url: AnyHttpUrl
    slug: str


class ShortenedUrl(ShortenedUrlBase):
    """
    Модель сокращённой ссылки
    """
