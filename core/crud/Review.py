from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas import CreateReview, ReviewResponse
from core import Review


async def create_review(
        review: CreateReview,
        session: AsyncSession
) -> ReviewResponse:
    try:
        created_review = Review(**review.model_dump())
        session.add(created_review)

        await session.commit()
        await session.refresh(created_review)
        return ReviewResponse.model_validate(created_review)

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


async def delete_review(
        review_id: int,
        session: AsyncSession,
):
    try:
        review = await session.get(Review, review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review does not exist"
            )
        await session.delete(review)
        await session.commit()

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


async def get_review(
        review_id: int,
        session: AsyncSession,
):
    try:
        review = await session.get(Review, review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review does not exist"
            )

        return ReviewResponse.model_validate(review)

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


async def get_review_by_book(
        book_id: int,
        skip: int,
        limit: int,
        session: AsyncSession
):
    try:
        stmt = select(Review).where(Review.book_id == book_id).offset(skip).limit(limit)
        asnw = await session.execute(stmt)
        reviews = asnw.scalars().all()
        return [ReviewResponse.model_validate(review) for review in reviews]

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
