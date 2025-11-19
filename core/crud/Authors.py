from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas import AuthorCreate, AuthorUpdate, AuthorResponse
from core import Author


async def create_author(
        author_create: AuthorCreate,
        session: AsyncSession
) -> AuthorResponse:
    try:
        stmt = select(Author).where(
            Author.first_name == author_create.first_name,
            Author.second_name == author_create.second_name,
        )
        found_author = await session.execute(stmt)

        if found_author.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Author is allready registred")

        author = Author(**author_create.model_dump())
        session.add(author)

        await session.commit()
        await session.refresh(author)

        return AuthorResponse.model_validate(author)

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


async def get_author_by_id(
        author_id: int,
        session: AsyncSession,
) -> AuthorResponse:
    try:
        author = await session.get(Author, author_id)
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Author does not exist"
            )
        return AuthorResponse.model_validate(author)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


async def get_authors_by_name(
        author_name: str,
        session: AsyncSession,
) -> list[AuthorResponse]:
    try:
        stmt = select(Author).where(Author.first_name == author_name)
        answ = await session.execute(stmt)
        authors = answ.scalars().all()
        return [AuthorResponse.model_validate(author) for author in authors]
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


async def update_author(
        author_id: int,
        author_update: AuthorUpdate,
        session: AsyncSession
) -> AuthorResponse:
    try:
        author = await session.get(Author, author_id)

        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Author does not exist"
            )

        updated_data = author_update.model_dump(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(author, key, value)

        await session.commit()
        await session.refresh(author)
        return AuthorResponse.model_validate(author)
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


async def delete_author(
        author_id: int,
        session: AsyncSession
):
    try:
        author = await session.get(Author, author_id)
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Author does not exist"
            )

        await session.delete(author)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

