import jwt


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
