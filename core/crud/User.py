from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core import User
from core.schemas import UserResponse, UpdateUser, CreateUser, LoginUser, Token, TokenData
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



async def create_user(
        user_data: CreateUser,
        session: AsyncSession
) -> UserResponse:
    stmt = select(User).where(User.username == user_data.username)
    find_user = await session.execute(stmt)
    if find_user.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username already registered"
        )

    user_data.password = get_password_hash(user_data.password)
    user = User(**user_data.dict())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return UserResponse.model_validate(user)


async def get_user_for_login(
    user_data: LoginUser,
    session: AsyncSession,
):
    stmt = select(User).where(User.username == user_data.username)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    if verify_password(user_data.password, user.password):
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
