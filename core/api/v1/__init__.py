from .Book import router as book_router
from .Author import router as author_router
from fastapi import APIRouter


router = APIRouter(prefix="/v1")
router.include_router(book_router)
router.include_router(author_router)


__all__ = [
    "router"
]
