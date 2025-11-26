import jwt
from fastapi import Request, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta, datetime, timezone

from core import User
from core.settings import settings

from core.database import get_db
from core.schemas import TokenData


def create_access_token(data: dict, expires_delta=None):
    data_dict = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    data_dict["exp"] = expire
    data_dict["type"] = "access"
    return jwt.encode(data_dict, settings.JWT_PRIVATE_KEY.read_text(), algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict, expires_delta=None):
    data_dict = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_DAYS*24*60))
    data_dict["exp"] = expire
    data_dict["type"] = "refresh"
    return jwt.encode(data_dict, settings.JWT_PRIVATE_KEY.read_text(), algorithm=settings.ALGORITHM)


def decode_token(token: str):
    from core.settings import settings
    try:
        return jwt.decode(token, settings.JWT_PUBLIC_KEY.read_text(), algorithms=[settings.ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token decoding error")


async def refresh_tokens_logic(
        request: Request,
        response: Response,
        refresh_token: str,
        session: AsyncSession
) -> tuple[TokenData, str]:
    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user = await session.get(User, int(user_id))
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        new_access_token = create_access_token(data={
            "sub": str(user.id),
            "username": user.username,
            "is_reader": user.is_reader,
            "is_author": user.is_author,
            "is_admin": user.is_admin,
        })

        new_refresh_token = create_refresh_token({
            "sub": str(user.id),
        })

        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            path="/"
        )

        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            path="/auth/refresh"
        )

        return (
            TokenData(
                sub=user.id,
                username=user.username,
                is_reader=user.is_reader,
                is_author=user.is_author,
                is_admin=user.is_admin,
            ),
            new_refresh_token
        )

    except Exception as e:
        raise HTTPException(status_code=401, detail="Refresh failed")


async def get_current_user_with_refresh(
        request: Request,
        response: Response,
        session: AsyncSession = Depends(get_db)
) -> TokenData:
    try:
        token = request.cookies.get("access_token")
        payload = decode_token(token)

        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )

        return TokenData(
            sub=int(payload["sub"]),
            username=payload["username"],
            is_reader=payload.get("is_reader", False),
            is_author=payload.get("is_author", False),
            is_admin=payload.get("is_admin", False),
        )
    except HTTPException as e:
        if e.status_code == 401 and "expired" in str(e.detail).lower():
            refresh_token = request.cookies.get("refresh_token")
            if refresh_token:
                try:
                    user_data, _ = await refresh_tokens_logic(
                        request=request,
                        response=response,
                        refresh_token=refresh_token,
                        session=session
                    )
                    return user_data
                except Exception as refresh_error:
                    print(f"Token refresh failed: {refresh_error}")
                    raise HTTPException(
                        status_code=401,
                        detail="Session expired. Please login again."
                    )
        raise e


async def get_current_user_from_cookie(
        request: Request,
) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    token = request.cookies.get("access_token")
    if not token:
        raise credentials_exception

    try:
        payload = decode_token(token)

        return TokenData(
            sub=int(payload["sub"]),
            username=payload["username"],
            is_reader=payload.get("is_reader", False),
            is_author=payload.get("is_author", False),
            is_admin=payload.get("is_admin", False),
        )

    except Exception:
        raise credentials_exception


async def get_current_reader(current_user: TokenData = Depends(get_current_user_with_refresh)):
    if not current_user.is_reader:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this operation"
        )
    return current_user


async def get_current_author(current_user: TokenData = Depends(get_current_user_with_refresh)):
    if not current_user.is_author:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this operation"
        )
    return current_user


async def get_current_admin(current_user: TokenData = Depends(get_current_user_with_refresh)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this operation"
        )
    return current_user
