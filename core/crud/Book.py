from fastapi import HTTPException, status
from sqlalchemy import select, func
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
    return books


async def delete_book_by_id(
        book_id: int,
        session: AsyncSession
):
    book = await session.get(Book, book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    await session.delete(book)
    await session.commit()


async def get_book_by_isbn(
        isbn: str,
        session: AsyncSession
):
    std = select(Book).where(Book.isbn == isbn)
    answ = await session.execute(std)
    books = answ.scalars().all()
    if not books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return books


async def get_book_paginated(
        session: AsyncSession,
        skip: int,
        limit: int,
):
    count_stmt = select(func.count(Book.id))
    total_result = await session.execute(count_stmt)
    total_count = total_result.scalar()

    stmt = select(Book).offset(skip).limit(limit)
    result = await session.execute(stmt)
    books = result.scalars().all()

    return {
        "items": books,
        "total": total_count,
        "skip": skip,
        "limit": limit,
        "has_more": skip+limit < total_count,
    }
