from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas import BookCreate, BookResponse
from core import Book
from core.database import get_db


from fastapi import APIRouter, Depends

router = APIRouter(prefix='/book', tags=['books'])


@router.post('/', response_model=BookResponse, status_code=201)
async def create_book(
        book: BookCreate,
        session: AsyncSession = Depends(get_db)
):
    db_book = Book(**book.model_dump())
    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)
    return db_book


@router.get('/{title}/', response_model=list[BookResponse])
async def get_book(
        title: str,
        session: AsyncSession = Depends(get_db)
):
    std = select(Book).where(Book.title == title)
    asnw = await session.execute(std)
    return asnw.scalars().all()
