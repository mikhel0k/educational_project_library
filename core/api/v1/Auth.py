from fastapi import APIRouter, Depends, Response, Request, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core import User
from core.database import get_db
from core.schemas import UserResponse, CreateUser, LoginUser
from core.crud import get_user_for_login, create_user
from core.dependencies import create_access_token, decode_token
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


@router.get("/check", response_model=UserResponse)
async def get_current_user_from_cookie(
        request: Request,
        session: AsyncSession = Depends(get_db)
) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    # Получаем токен из куки
    token = request.cookies.get("access_token")

    if not token:
        raise credentials_exception

    try:
        payload = decode_token(token)
        username = payload.get("sub")

        if username is None:
            raise credentials_exception

        stmt = select(User).where(User.username == username)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None:
            raise credentials_exception

        return UserResponse.model_validate(user)

    except Exception:
        raise credentials_exception
