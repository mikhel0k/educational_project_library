from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import book_create, get_book_by_title, delete_book_by_id, get_book_paginated

from core.schemas import BookCreate, BookResponse
from core.database import get_db

from fastapi import APIRouter, Depends


router = APIRouter(prefix='/book', tags=['books'])


@router.post('/', response_model=BookResponse, status_code=201)
async def create_book(
        book: BookCreate,
        session: AsyncSession = Depends(get_db)
):
    book = await book_create(
        book=book,
        session=session
    )
    return book


@router.get('/{title}/', response_model=list[BookResponse])
async def get_book(
        title: str,
        session: AsyncSession = Depends(get_db)
):
    return await get_book_by_title(title, session)


@router.delete('/{book_id}')
async def delete_book(
        book_id: int,
        session: AsyncSession = Depends(get_db)
):
    await delete_book_by_id(book_id, session)


@router.get('/books')
async def get_books(
        limit: int = 30,
        offset: int = 0,
        session: AsyncSession = Depends(get_db)
):
    return await get_book_paginated(session, offset, limit)
