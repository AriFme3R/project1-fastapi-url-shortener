from pydantic import BaseModel


class MovieBase(BaseModel):
    id: int
    title: str
    description: str
    year: int
    duration: int


class Movie(MovieBase):
    """
    Модель фильма
    """
