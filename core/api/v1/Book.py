from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from core.crud import read_book_by_title, read_books, read_book_by_isbn, delete_book, create_book
from core.schemas import BookCreate, BookResponse
from core.database import get_db


router = APIRouter(prefix="/books", tags=["books"])


@router.get("/search/title/{title}", response_model=list[BookResponse])
async def search_books_by_title(
    title: str,
    session: AsyncSession = Depends(get_db)
) -> list[BookResponse]:
    return await read_book_by_title(title, session)


@router.get("/search/isbn/{isbn}", response_model=BookResponse)
async def get_book_by_isbn(
    isbn: str,
    session: AsyncSession = Depends(get_db)
) -> BookResponse:
    return await read_book_by_isbn(isbn, session)


@router.get("/", response_model=Dict[str, Any])
async def get_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(30, ge=0, le=100),
    session: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    return await read_books(session, skip, limit)


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def post_book(
    book: BookCreate,
    session: AsyncSession = Depends(get_db)
) -> BookResponse:
    return await create_book(book=book, session=session)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_by_id(
    book_id: int,
    session: AsyncSession = Depends(get_db)
):
    await delete_book(book_id, session)
