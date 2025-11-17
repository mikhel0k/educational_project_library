from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core import Book
from core.database import get_db
from core.schemas import BookCreate


async def book_create(
        book: BookCreate,
        session: AsyncSession,
):
    std = select(Book).where(Book.isbn == book.isbn)
    answ = await session.execute(std)
    books = answ.scalars().all()
    if books:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book is already registered"
        )

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
    answ = await session.execute(std)
    books = answ.scalars().all()
    if not books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return answ.scalars().all()


async def delete_book_by_id(
        book_id: int,
        session: AsyncSession
):
    book = await session.get(Book, book_id)
    await session.delete(book)
    await session.commit()
