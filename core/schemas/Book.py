from datetime import date, datetime

from pydantic import BaseModel, Field, ConfigDict


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


class BookCreate(BookBase):
    pass


class BookResponse(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
