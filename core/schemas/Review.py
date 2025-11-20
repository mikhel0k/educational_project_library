from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    user_name: str
    title: Optional[str] = None
    review_text: str
    book_id: int


class CreateReview(BaseSchema):
    pass


class ReviewResponse(BaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
