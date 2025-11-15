from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from ..settings import get_db_url


async_engine = create_async_engine(get_db_url())

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
