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


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    first_name: str | None
    second_name: str | None
    email: EmailStr

    id: int
    is_reader: bool
    is_author: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime


class LoginUser(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
