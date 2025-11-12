from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .Base import BaseModel


class PhysicalBook(BaseModel):
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'), nullable=False)
    isbn: Mapped[str] = mapped_column(String(20), nullable=False)
    publisher: Mapped[str] = mapped_column(String(128), nullable=False)
    edition: Mapped[str | None] = mapped_column(String(128), nullable=True)
    condition: Mapped[str] = mapped_column(String(128), nullable=False)

    def __str__(self):
        return f'{self.isbn} {self.publisher} {self.edition}: {self.condition}'

    def __repr__(self):
        return str(self)
