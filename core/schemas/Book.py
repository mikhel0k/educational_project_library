from datetime import date, datetime
from typing import List

from pydantic import BaseModel, Field, ConfigDict

from .Author import AuthorResponse
from .Review import ReviewResponse


class BookBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=128,
        description="The title of the book"
    )
    isbn: str = Field(
        ...,
        min_length=10,
        max_length=13,
        pattern=r"^\d{10,13}$",
        description="ISBN of the book"
    )
    publication_year: date = Field(
        ...,
        description="year of the book publication",
    )
    author_id: int = Field(
        ...,
        description="author_id of the book"
    )


class BookCreate(BookBase):
    pass


class BookResponse(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    author: AuthorResponse
    reviews: List[ReviewResponse]
