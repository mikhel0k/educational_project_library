from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.schemas import AuthorCreate, AuthorUpdate, AuthorResponse
from core.database import get_db
from core.crud import delete_author, create_author, update_author, get_author_by_id, get_authors_by_name


router = APIRouter(prefix="/authors", tags=["authors"])


@router.get("/id/{author_id}", response_model=AuthorResponse)
async def author_get_by_id(
        author_id: int,
        session: AsyncSession = Depends(get_db)
):
    author = await get_author_by_id(author_id, session)
    return author


@router.get("/name/{author_name}", response_model=list[AuthorResponse])
async def author_get_by_name(
        author_name: str,
        session: AsyncSession = Depends(get_db)
):
    author = await get_authors_by_name(author_name, session)
    return author


@router.post("/", response_model=AuthorResponse)
async def author_create(
        author: AuthorCreate,
        session: AsyncSession = Depends(get_db)
):
    author = await create_author(author, session)
    return author


@router.put("/{author_id}", response_model=AuthorResponse)
async def author_update(
        author_id: int,
        author: AuthorUpdate,
        session: AsyncSession = Depends(get_db)
):
    author = await update_author(author_id, author, session)
    return author


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def author_delete(
        author_id: int,
        session: AsyncSession = Depends(get_db)
):
    author = await delete_author(author_id, session)
    return author
