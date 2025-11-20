from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.schemas import CreateReview, ReviewResponse
from core import Review


async def create_review(
        review: CreateReview,
        session: AsyncSession
) -> ReviewResponse:
    created_review = Review(**review.model_dump())
    session.add(created_review)
    await session.commit()
    await session.refresh(created_review)
    return ReviewResponse.model_validate(created_review)


async def delete_review(
        review_id: int,
        session: AsyncSession,
):
    review = await session.get(Review, review_id)
    await session.delete(review)
    await session.commit()


async def get_review(
        review_id: int,
        session: AsyncSession,
):
    review = await session.get(Review, review_id)
    return ReviewResponse.model_validate(review)


async def get_review_by_book(
        book_id: int,
        skip: int,
        limit: int,
        session: AsyncSession
):
    stmt = select(Review).where(Review.book_id == book_id).offset(skip).limit(limit)
    asnw = await session.execute(stmt)
    reviews = asnw.scalars().all()
    return [ReviewResponse.model_validate(review) for review in reviews]
