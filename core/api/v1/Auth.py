from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.schemas import UserResponse, CreateUser, LoginUser
from core.crud import get_user_for_login, create_user
from core.dependencies import create_access_token
from core.settings import settings


router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/registration")
async def register(
        user: CreateUser,
        session: AsyncSession = Depends(get_db)
):
    await create_user(user, session)
    return {"message": "User created successfully"}


@router.post("/login")
async def get_current_user(
        response: Response,
        user_data: LoginUser,
        session: AsyncSession = Depends(get_db)
):
    user = await get_user_for_login(user_data, session)

    token = create_access_token(
        data={
            "sub": user.username,
        }
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES*60,
        path="/"
    )
    return "Logged in successfully"
