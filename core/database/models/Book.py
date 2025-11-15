from datetime import date

from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column

from .BaseModel import BaseModel


class Book(BaseModel):
    __tablename__ = 'books'

    title: Mapped[str] = mapped_column(String(128), nullable=False)
    isbn: Mapped[str] = mapped_column(String(17), nullable=False)
    publication_year: Mapped[date] = mapped_column(Date, nullable=False)
