from sqlalchemy import ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .Base import BaseModel


class BookCopy(BaseModel):
    __tablename__ = 'book_copies'

    physical_book_id: Mapped[str] = mapped_column(ForeignKey('physical_books.id'), nullable=False)
    copy_number: Mapped[str] = mapped_column(String(50), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    notes: Mapped[str | None] = mapped_column(String(255), nullable=True)

    physical_book: Mapped["PhysicalBook"] = relationship("PhysicalBook", back_populates="copies")
