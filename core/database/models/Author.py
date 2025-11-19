from datetime import datetime

from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .BaseModel import BaseModel


class Author(BaseModel):
    __tablename__ = 'authors'
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    second_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    birth_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    bio: Mapped[str | None] = mapped_column(Text(), nullable=True)

    books: Mapped[list["Book"]] = relationship("Book", back_populates="author")
