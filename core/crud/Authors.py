from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas import AuthorCreate, AuthorUpdate, AuthorResponse
from core import Author


async def create_author(
        author_create: AuthorCreate,
        session: AsyncSession
) -> AuthorResponse:
    author = Author(**author_create.model_dump())
    session.add(author)
    await session.commit()
    await session.refresh(author)
    return AuthorResponse.model_validate(author)


async def get_author_by_id(
        author_id: int,
        session: AsyncSession,
) -> AuthorResponse | None:
    author = await session.get(Author, author_id)
    return AuthorResponse.model_validate(author) if author else None


async def get_authors_by_name(
        author_name: str,
        session: AsyncSession,
) -> [AuthorResponse]:
    stmt = select(Author).where(Author.first_name == author_name)
    answ = await session.execute(stmt)
    authors = answ.scalars().all()
    return [AuthorResponse.model_validate(author) for author in authors]


async def update_author(
        author_id: int,
        author_update: AuthorUpdate,
        session: AsyncSession
) -> AuthorResponse:
    author = await session.get(Author, author_id)

    updated_data = author_update.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(author, key, value)

    await session.commit()
    await session.refresh(author)
    return AuthorResponse.model_validate(author)


async def delete_author(
        author_id: int,
        session: AsyncSession
):
    author = await session.get(Author, author_id)
    await session.delete(author)
    await session.commit()
