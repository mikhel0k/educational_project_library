from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from core import User
from core.crud import create_review, delete_review, read_review_by_id, read_review_by_book
from core.database import get_db
from core.dependencies import get_current_reader, get_current_admin
from core.schemas import ReviewResponse, CreateReview, TokenData

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/{review_id}", response_model=ReviewResponse)
async def get_review(
    review_id: int,
    session: AsyncSession = Depends(get_db)
) -> ReviewResponse:
    return await read_review_by_id(review_id, session)


@router.get("/book/{book_id}", response_model=Dict[str, Any])
async def get_book_reviews(
    book_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(30, ge=0, le=100),
    session: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    return await read_review_by_book(book_id, skip, limit, session)


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def post_review(
    review: CreateReview,
    user: TokenData = Depends(get_current_reader),
    session: AsyncSession = Depends(get_db)
) -> ReviewResponse:
    return await create_review(review, session)


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review_by_id(
    review_id: int,
    user: TokenData = Depends(get_current_admin),
    session: AsyncSession = Depends(get_db)
):
    await delete_review(review_id, session)
