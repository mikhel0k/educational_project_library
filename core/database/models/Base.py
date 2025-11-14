from datetime import datetime

from sqlalchemy import Integer, DateTime, func
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls):
        name = cls.__name__
        if name == 'Base':
            return None
        snake_case = ''.join(['_' + i.lower() if i.isupper() else i for i in name]).lstrip('_')
        return snake_case + 's'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False,
    )
