from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped


class BaseModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    created_at: Mapped[datetime] = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now,
        nullable=False,
    )
