from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core import Book
from core.database import get_db
from core.schemas import BookCreate


async def book_create(
        book: BookCreate,
        session: AsyncSession,
):
    db_book = Book(**book.model_dump())
    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)
    return db_book


async def get_book_by_title(
        title: str,
        session: AsyncSession
):
    std = select(Book).where(Book.title == title)
    asnw = await session.execute(std)
    return asnw.scalars().all()


async def delete_book_by_id(
        book_id: int,
        session: AsyncSession
):
    book = await session.get(Book, book_id)
    await session.delete(book)
    await session.commit()
