from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .Base import BaseModel


class Ebook(BaseModel):
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'), nullable=False)
    file_format: Mapped[str] = mapped_column(String(10), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    download_link: Mapped[str] = mapped_column(String(255), nullable=False)
    compatible_devices: Mapped[str | None] = mapped_column(String(255), nullable=True)

    def __str__(self):
        return f'{self.book_id}: {self.file_format} | {self.file_size} | {self.download_link}'

    def __repr__(self):
        return str(self)
