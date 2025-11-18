from typing import Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.crud import book_create, get_book_by_title, delete_book_by_id, get_book_paginated, get_book_by_isbn

from core.schemas import BookCreate, BookResponse
from core.database import get_db

from fastapi import APIRouter, Depends, Query

router = APIRouter(prefix='/book', tags=['books'])


@router.get('/get_by_title/{title}', response_model=list[BookResponse])
async def get_book_by_title(
        title: str,
        session: AsyncSession = Depends(get_db)
):
    return await get_book_by_title(title, session)


@router.get('/get_by_isbn/{isbn}', response_model=list[BookResponse])
async def get_book_by_isbn(
        isbn: str,
        session: AsyncSession = Depends(get_db)
):
    return await get_book_by_isbn(isbn, session)


@router.get('/books', response_model=Dict[str, Any])
async def get_books(
        skip: int = Query(0, ge=0, description="Number of books to skip"),
        limit: int = Query(30, ge=0, le=100, description="Number of books to return"),
        session: AsyncSession = Depends(get_db)
):
    return await get_book_paginated(session, skip, limit)


@router.post('/create', response_model=BookResponse, status_code=201)
async def create_book(
        book: BookCreate,
        session: AsyncSession = Depends(get_db)
):
    book = await book_create(
        book=book,
        session=session
    )
    return book


@router.delete('/delete/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
        book_id: int,
        session: AsyncSession = Depends(get_db)
):
    await delete_book_by_id(book_id, session)
