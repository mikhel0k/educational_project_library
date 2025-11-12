from datetime import datetime

from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .Base import BaseModel


class Author(BaseModel):
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    birth_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    nationality: Mapped[str] = mapped_column(String(50), nullable=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}: {self.birth_date} - {self.nationality}'

    def __repr__(self):
        return str(self)
