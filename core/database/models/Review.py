from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .BaseModel import BaseModel


class Review(BaseModel):
    __tablename__ = "reviews"

    user_name: Mapped[str] = mapped_column(String, nullable=False, default='User')
    title: Mapped[str | None] = mapped_column(String, nullable=True)
    review_text: Mapped[str] = mapped_column(Text, nullable=False)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey('books.id'), nullable=False)

    book: Mapped["Book"] = relationship("Book", back_populates="reviews")
