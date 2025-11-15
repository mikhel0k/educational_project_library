from .Book import router as book_router
from fastapi import APIRouter


router = APIRouter(prefix="/v1")
router.include_router(book_router)


__all__ = [
    "router"
]
