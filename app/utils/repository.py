from abc import ABC, abstractmethod

from sqlalchemy import insert, select, delete
from app.database.session import async_session


class AbstractRepository(ABC):

    @abstractmethod
    async def add_one(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_filter(self, *args, **kwargs):
        raise NotImplementedError

    async def delete(self, *args, **kwargs):
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

    async def get_all_by_filter(self, *args, **kwargs) -> list:
        async with async_session() as session:
            async with session.begin():
                stmt = await session.execute(
                    select(self.model).filter_by(user=kwargs.get('user'))
                )
                return [result[0] for result in stmt.all()]

    async def delete(self, *args, **kwargs) -> int:
        async with async_session() as session:
            async with session.begin():
                stmt = await session.execute(
                    delete(self.model).filter_by(id=kwargs.get('id')).\
                    returning(self.model.id)
                )
                return stmt.scalars().first()