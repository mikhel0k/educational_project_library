from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .Base import BaseModel


class Review(BaseModel):
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'), nullable=False)
    rating: Mapped[int] = mapped_column(Integer(), nullable=False)
    comment: Mapped[str] = mapped_column(Text(), nullable=False)

    def __str__(self):
        return f'{self.rating} - {self.comment}'

    def __repr__(self):
        return str(self)
