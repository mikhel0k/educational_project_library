from typing import Dict, Any, List

from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas import BookCreate, BookResponse
from core import Book


async def read_book_by_title(
        title: str,
        session: AsyncSession
) -> List[BookResponse]:
    try:
        stmt = select(Book).where(Book.title == title)
        answ = await session.execute(stmt)
        books = answ.scalars().all()
        if not books:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        return [BookResponse.model_validate(book) for book in books]
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


async def read_book_by_isbn(
        isbn: str,
        session: AsyncSession
) -> BookResponse:
    try:
        stmt = select(Book).where(Book.isbn == isbn)
        answ = await session.execute(stmt)
        book = answ.scalar_one_or_none()
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        return BookResponse.model_validate(book)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


async def read_books(
        session: AsyncSession,
        skip: int,
        limit: int,
) -> Dict[str, Any]:
    try:
        count_stmt = select(func.count(Book.id))
        total_result = await session.execute(count_stmt)
        total_count = total_result.scalar()

        stmt = select(Book).offset(skip).limit(limit)
        result = await session.execute(stmt)
        books = result.scalars().all()
        books_schemas = [BookResponse.model_validate(book) for book in books]

        return {
            "items": books_schemas,
            "total": total_count,
            "skip": skip,
            "limit": limit,
            "has_more": skip+limit < total_count,
        }
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


async def create_book(
        book: BookCreate,
        session: AsyncSession,
) -> BookResponse:
    try:
        stmt = select(Book).where(Book.isbn == book.isbn)
        answ = await session.execute(stmt)
        if answ.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book is already registered"
            )

        db_book = Book(**book.model_dump())
        session.add(db_book)

        await session.commit()
        await session.refresh(db_book)
        return BookResponse.model_validate(db_book)

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


async def delete_book(
        book_id: int,
        session: AsyncSession
):
    try:
        book = await session.get(Book, book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book does not exist"
            )

        await session.delete(book)
        await session.commit()

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
