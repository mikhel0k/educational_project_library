from sqlalchemy.ext.asyncio import create_async_engine
from ..settings import get_db_url


async_engine = create_async_engine()
