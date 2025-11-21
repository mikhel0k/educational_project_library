from pydantic import EmailStr
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .BaseModel import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str | None] = mapped_column(String, nullable=True)
    second_name: Mapped[str | None] = mapped_column(String, nullable=True)
    email: Mapped[EmailStr] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
