from typing import Dict, Any

from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas import CreateReview, ReviewResponse
from core import Review


async def read_review_by_id(
        review_id: int,
        session: AsyncSession,
) -> ReviewResponse:
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


async def read_review_by_book(
        book_id: int,
        skip: int,
        limit: int,
        session: AsyncSession
) -> Dict[str, Any]:
    try:
        count_stmt = select(func.count(Review.id)).where(Review.book_id == book_id)
        total_result = await session.execute(count_stmt)
        total_count = total_result.scalar()

        stmt = select(Review).where(Review.book_id == book_id).offset(skip).limit(limit)
        answ = await session.execute(stmt)
        reviews = answ.scalars().all()
        reviews_schema = [ReviewResponse.model_validate(review) for review in reviews]
        return {
            "items": reviews_schema,
            "total": total_count,
            "skip": skip,
            "limit": limit,
            "has_more": skip + limit < total_count,
        }

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


async def create_review(
        review: CreateReview,
        session: AsyncSession
) -> ReviewResponse:
    try:
        db_review = Review(**review.model_dump())
        session.add(db_review)

        await session.commit()
        await session.refresh(db_review)
        return ReviewResponse.model_validate(db_review)

    except SQLAlchemyError as e:
        await session.rollback()
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
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
