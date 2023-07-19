from abc import ABC, abstractmethod

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import async_session


class AbstractRepository(ABC):

    @abstractmethod
    async def add_one(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, **kwargs):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):

    model = None

    async def add_one(self, **kwargs) -> int:
        async with async_session() as session:
            async with session.begin():
                stmt = await session.execute(
                    insert(self.model).values(kwargs).returning(self.model.id)
                )
                return stmt.scalars().first()

    async def get_one(self, session: AsyncSession, **kwargs):
        stmt = await session.execute(
            select(self.model).filter_by(id=kwargs.get('id'))
        )
        return stmt.first()