from datetime import date

from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .BaseModel import BaseModel


class Book(BaseModel):
    __tablename__ = 'books'

    title: Mapped[str] = mapped_column(String(128), nullable=False)
    isbn: Mapped[str] = mapped_column(String(17), nullable=False)
    publication_year: Mapped[date] = mapped_column(Date, nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id'), nullable=False)

    author: Mapped["Author"] = relationship("Author", back_populates="books")
