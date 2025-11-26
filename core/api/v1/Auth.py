from fastapi import APIRouter, Depends, Response, Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core import User
from core.database import get_db
from core.schemas import UserResponse, CreateUser, LoginUser, Token
from core.crud import get_user_for_login, create_user
from core.dependencies import create_access_token, get_current_user_from_cookie, create_refresh_token, decode_token
from core.schemas.User import RefreshToken
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

    access_token = create_access_token(data={
        "sub": str(user.id),
        "username": user.username,
        "is_reader": user.is_reader,
        "is_author": user.is_author,
        "is_admin": user.is_admin,
    })

    refresh_token = create_refresh_token({
        "sub": str(user.id),
    })

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/"
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/auth/refresh"
    )

    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=Token)
async def refresh(
        request: Request,
        response: Response,
        refresh_data: RefreshToken = None,
        session: AsyncSession = Depends(get_db)
):
    refresh_token = refresh_data.refresh_token if refresh_data else request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token required"
        )

    try:
        from core.dependencies import refresh_tokens_logic
        user_data, new_refresh_token = await refresh_tokens_logic(
            request, response, refresh_token, session
        )

        new_access_token = create_access_token(data={
            "sub": str(user_data.sub),
            "username": user_data.username,
            "is_reader": user_data.is_reader,
            "is_author": user_data.is_author,
            "is_admin": user_data.is_admin,
        })

        return Token(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="Bearer"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token", path="/")
    response.delete_cookie(key="refresh_token", path="/auth/refresh")
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserResponse = Depends(get_current_user_from_cookie)):
    return current_user

