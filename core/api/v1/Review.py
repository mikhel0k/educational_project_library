from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.crud import create_review, get_review, delete_review, get_review_by_book
from core.database import get_db
from core.schemas import ReviewResponse, CreateReview
from core import Review

router = APIRouter(prefix="/review", tags=["reviews"])


@router.get("/id/{review_id}", response_model=ReviewResponse)
async def get_review_by_id(
        review_id: int,
        session: AsyncSession = Depends(get_db)
) -> ReviewResponse:
    review = await get_review(review_id, session)
    return review


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def post_review(
        created_review: CreateReview,
        session: AsyncSession = Depends(get_db)
) -> ReviewResponse:
    review = await create_review(created_review, session)
    return review


@router.get("/book/{book_id}", response_model=list[ReviewResponse])
async def get_reviews_for_book(
        book_id: int,
        skip: int = Query(0, ge=0),
        limit: int = Query(30, ge=0, le=100),
        session: AsyncSession = Depends(get_db)
) -> list[ReviewResponse]:
    reviews = await get_review_by_book(book_id, skip, limit, session)
    return reviews


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review_by_id(
        review_id: int, session: AsyncSession = Depends(get_db)
):
    review = await delete_review(review_id, session)
