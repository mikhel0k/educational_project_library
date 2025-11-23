from datetime import timedelta, datetime, timezone

from jose import jwt
from passlib.context import CryptContext
from core.settings import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_PRIVATE_KEY = settings.JWT_PRIVATE_KEY.read_text()
JWT_PUBLIC_KEY = settings.JWT_PUBLIC_KEY.read_text()
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
ALGORITHM = settings.ALGORITHM


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    data_dict = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    data_dict["exp"] = expire
    encoded_jwt = jwt.encode(data_dict, JWT_PRIVATE_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    try:
        payload = jwt.decode(token, JWT_PUBLIC_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError as e:
        raise e
