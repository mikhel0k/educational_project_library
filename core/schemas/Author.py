from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class BaseSchema(BaseModel):
    first_name: str = Field(..., description="First Name")
    second_name: str | None = Field(..., description="Second Name")
    birth_date: datetime = Field(..., description="Birthday date")
    bio: str | None = Field(..., description="Bio of author")


class AuthorCreate(BaseSchema):
    pass


class AuthorUpdate(BaseModel):
    first_name: str | None = Field(None, description="First Name")
    second_name: str | None = Field(None, description="Second Name")
    birth_date: datetime | None = Field(None, description="Birthday date")
    bio: str | None = Field(None, description="Bio of author")


class AuthorResponse(BaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
