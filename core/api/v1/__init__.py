from .Book import router as book_router
from .Author import router as author_router
from .Review import router as review_router
from .Auth import router as auth_router
from fastapi import APIRouter


router = APIRouter(prefix="/v1")
router.include_router(book_router)
router.include_router(author_router)
router.include_router(review_router)
router.include_router(auth_router)


__all__ = [
    "router"
]
