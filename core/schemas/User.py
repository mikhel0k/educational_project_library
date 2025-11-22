from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str


class UpdateUser(BaseModel):
    first_name: str | None
    second_name: str | None
    email: EmailStr | None


class UserResponce(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    first_name: str | None
    second_name: str | None
    email: EmailStr

    id: int
    created_at: datetime
    updated_at: datetime
