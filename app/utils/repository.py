from abc import ABC, abstractmethod

from sqlalchemy import insert, select
from app.database.session import async_session


class AbstractRepository(ABC):

    @abstractmethod
    async def add_one(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, *args, **kwargs):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):

    model = None

    async def add_one(self, **kwargs):
        async with async_session() as session:
            async with session.begin():
                stmt = await session.execute(
                    insert(self.model).values(kwargs).returning(self.model)
                )
                return stmt.scalars().first()

    async def get_one(self, **kwargs):
        async with async_session() as session:
            async with session.begin():
                stmt = await session.execute(
                    select(self.model).filter_by(name_file=kwargs.get('name_file'), user=kwargs.get('user'))
                )
                return stmt.scalars().first()