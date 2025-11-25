import jwt
from fastapi import Request, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core import User
from core.database import get_db
from core.schemas import TokenData


def create_access_token(data: dict, expires_delta=None):
    from datetime import timedelta, datetime, timezone
    from core.settings import settings

    data_dict = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    data_dict["exp"] = expire
    return jwt.encode(data_dict, settings.JWT_PRIVATE_KEY.read_text(), algorithm=settings.ALGORITHM)


def decode_token(token: str):
    from core.settings import settings
    try:
        return jwt.decode(token, settings.JWT_PUBLIC_KEY.read_text(), algorithms=[settings.ALGORITHM])
    except Exception as e:
        raise e


async def get_current_user_from_cookie(
        request: Request,
        session: AsyncSession = Depends(get_db)
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
        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        return TokenData.model_validate(**payload)

    except Exception:
        raise credentials_exception


async def get_current_reader(current_user: TokenData = Depends(get_current_user_from_cookie)):
    if not current_user.is_reader:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this operation"
        )
    return current_user


async def get_current_author(current_user: TokenData = Depends(get_current_user_from_cookie)):
    if not current_user.is_author:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this operation"
        )
    return current_user


async def get_current_admin(current_user: TokenData = Depends(get_current_user_from_cookie)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this operation"
        )
    return current_user
