from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from ..settings import get_db_url


ASYNC_DATABASE_URL = get_db_url()

async_engine = create_async_engine(ASYNC_DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
