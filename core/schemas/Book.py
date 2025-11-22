from datetime import date, datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator

from .Author import AuthorResponse


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

    @field_validator("publication_year")
    def validate_publication_year(cls, v):
        if v > date.today().year:
            raise ValueError("Publication year cannot be in the future")
        return v


class BookCreate(BookBase):
    pass


class BookResponse(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    author: AuthorResponse


class BookMinimal(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    isbn: str
