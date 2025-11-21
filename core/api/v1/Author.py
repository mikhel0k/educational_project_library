from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas import AuthorCreate, AuthorUpdate, AuthorResponse
from core.database import get_db
from core.crud import delete_author, create_author, update_author, read_author_by_id, read_authors_by_name


router = APIRouter(prefix="/authors", tags=["authors"])


@router.get("/{author_id}", response_model=AuthorResponse)
async def get_author(
    author_id: int,
    session: AsyncSession = Depends(get_db)
) -> AuthorResponse:
    return await read_author_by_id(author_id, session)


@router.get("/search/{name}", response_model=list[AuthorResponse])
async def search_authors(
    name: str,
    session: AsyncSession = Depends(get_db)
) -> list[AuthorResponse]:
    return await read_authors_by_name(name, session)


@router.post("/", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED)
async def post_author(
    author: AuthorCreate,
    session: AsyncSession = Depends(get_db)
) -> AuthorResponse:
    return await create_author(author, session)


@router.patch("/{author_id}", response_model=AuthorResponse)
async def patch_author(
    author_id: int,
    author: AuthorUpdate,
    session: AsyncSession = Depends(get_db)
) -> AuthorResponse:
    return await update_author(author_id, author, session)


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author_by_id(
    author_id: int,
    session: AsyncSession = Depends(get_db)
):
    await delete_author(author_id, session)
