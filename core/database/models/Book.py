from sqlalchemy import String, Text, Float, Integer, Computed, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .Base import BaseModel


class Book(BaseModel):
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(Text(), nullable=True)
    publication_year: Mapped[int] = mapped_column(Integer, nullable=False)
    genre: Mapped[str] = mapped_column(String(128), nullable=False)
    language: Mapped[str] = mapped_column(String(128), nullable=False)

    physical_books: Mapped[list["PhysicalBook"]] = relationship("PhysicalBook", back_populates="book")
    ebook: Mapped["Ebook | None"] = relationship("Ebook", back_populates="book", uselist=False)
    audio_book: Mapped["AudioBook | None"] = relationship("AudioBook", back_populates="book", uselist=False)

    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="book")
    authors: Mapped[list["Author"]] = relationship("Author", secondary="BookAuthor", back_populates="books")

    def __str__(self):
        return (f"Title: {self.title} of {self.publication_year} year,"
                f"Genre: {self.genre}")

    def __repr__(self):
        return str(self)
