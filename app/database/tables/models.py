import datetime
import uuid
from fastapi import Depends
from sqlalchemy import String, Boolean, TIMESTAMP, UUID, ForeignKey, BINARY
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.generics import GUID
from app.database.session import get_db


Base = declarative_base()


class User(SQLAlchemyBaseUserTableUUID, Base):
    """
    Models User:
    Attributes:
        - id: pk, type UUID
        - email: unique email
        - register_at: datetime
        - hashed password: str
        - is_active: boolean
        - is_superuser: boolean
        - is_verified: boolean
    """
    id: Mapped[uuid.UUID] = mapped_column(
        GUID, primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(128), unique=True, nullable=False
    )
    register_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP, default=datetime.datetime.utcnow(),
        nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(128), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )


class AudioFile(Base):
    """
    Models AudioFile:
    Attributes:
        - id: pk, type UUID
        - user: ForeignKey, type UUID
        - data: Binary (скачивание на прямую из базы)
    """

    __tablename__ = 'audio_file'

    id: Mapped[uuid.UUID] = mapped_column(
       UUID, primary_key=True, default=uuid.uuid4
    )
    user: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey('user.id', ondelete='CASCADE')
    )
    data = mapped_column(
        BINARY, nullable=False
    )


async def get_user_db(session: AsyncSession = Depends(get_db)):
    yield SQLAlchemyUserDatabase(session, User)


