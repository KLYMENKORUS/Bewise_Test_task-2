import typing
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from db.dal import AudioDAL, UserDAL
from db.models import AudioFile, User


class UserAction:

    @classmethod
    async def get_user_by_id(
            cls, user_id: uuid.UUID,
            db_session: AsyncSession
    ) -> User | None:
        async with db_session as session:
            async with session.begin():
                user_dal = UserDAL(session)
                get_user = await user_dal.get_by_user_id(
                    user_id=user_id
                )
                return get_user


class AudioAction:

    @classmethod
    async def create_audio(
            cls, user_id: uuid.UUID,
            data: bytes,
            db_session: AsyncSession
    ) -> AudioFile:
        async with db_session as session:
            async with session.begin():
                audio_dal = AudioDAL(session)
                new_audiofile = await audio_dal.create_audio(
                    user_id=user_id,
                    data=data
                )
                return new_audiofile

    @classmethod
    async def get_by_user_audio_file(
            cls, user_id: uuid.UUID,
            file_id: uuid.UUID,
            db_session: AsyncSession
    ) -> AudioFile | None:
        async with db_session as session:
            async with session.begin():
                audio_dal = AudioDAL(session)
                get_audio = await audio_dal.get_by_user_audio_file(
                    user_id=user_id,
                    file_id=file_id
                )
                return get_audio

