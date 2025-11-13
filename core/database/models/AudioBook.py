from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .Base import BaseModel


class AudioBook(BaseModel):
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'), nullable=False)
    duration: Mapped[int] = mapped_column(Integer(), nullable=False)
    narrator: Mapped[str] = mapped_column(String(128), nullable=False, default="Неизвестный")
    audio_format: Mapped[str] = mapped_column(String(10), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer(), nullable=False)
    streaming_link: Mapped[str] = mapped_column(String(255), nullable=False)

    book: Mapped["Book"] = relationship("Book", back_populates="audio_book")

    def __str__(self):
        return f"{self.duration} {self.narrator} {self.audio_format} {self.file_size}"

    def __repr__(self):
        return str(self)
