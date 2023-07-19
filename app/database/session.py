from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.database import settings

# create async engine
engine = create_async_engine(settings.DATABASE_URL, future=True, echo=True)

# create session
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async setting"""
    async with async_session() as session:
        yield session