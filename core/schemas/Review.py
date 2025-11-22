from datetime import datetime
from pydantic import BaseModel, ConfigDict

from .Book import BookMinimal


class BaseSchema(BaseModel):
    user_name: str
    title: str | None = None
    review_text: str


class CreateReview(BaseSchema):
    book_id: int


class ReviewResponse(BaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    book: BookMinimal
