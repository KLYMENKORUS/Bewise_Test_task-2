import asyncio

import pytest
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine,\
    async_sessionmaker, AsyncSession

from app import create_app
from app.database.session import get_db
from app.database import metadata


app = create_app()


DATABASE_URL_TEST = 'postgresql+asyncpg://postgres_test:postgres_test@127.0.0.1:5436/Testdb'

# create async test engine
test_engine = create_async_engine(
    DATABASE_URL_TEST, future=True, echo=True, poolclass=NullPool
)

# create test session
test_async_session = async_sessionmaker(
    test_engine, expire_on_commit=False, class_=AsyncSession
)

metadata.bind = test_engine


async def get_async_test_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session() as session:
        yield session

app.dependency_overrides[get_db] = get_async_test_session


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)


# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Create a new FastAPI TestClient instance"""
    async with AsyncClient(app=app, base_url='http://test') as async_client:
        yield async_client



