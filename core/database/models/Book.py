from sqlalchemy import String, Text, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .Base import BaseModel


class Book(BaseModel):
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(Text(), nullable=True)
    publication_year: Mapped[int] = mapped_column(Integer, nullable=False)
    genre: Mapped[str] = mapped_column(String(128), nullable=False)
    language: Mapped[str] = mapped_column(String(128), nullable=False)
    average_rating: Mapped[float] = mapped_column(Float, default=0.0)

    physical_books: Mapped[list["PhysicalBook"]] = relationship("PhysicalBook", back_populates="book")
    ebook: Mapped["Ebook | None"] = relationship("Ebook", back_populates="book", uselist=False)
    audio_book: Mapped["AudioBook | None"] = relationship("AudioBook", back_populates="book", uselist=False)

    def __str__(self):
        return (f"Title: {self.title} of {self.publication_year} year,"
                f"Genre: {self.genre} ({self.average_rating:.2f}) ")

    def __repr__(self):
        return str(self)
