import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from db.models import AudioFile, User


class UserDAL:
    """Data Access layer for operating users info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_by_user_id(self, user_id: uuid.UUID) -> User | None:
        """
        Получение пользователя по его id
        : user_id: id
        : return: User | None
        """
        query = select(User).where(User.id == user_id)
        result = await self.db_session.execute(query)
        get_user = result.fetchall()

        return None if get_user is None else get_user[0]


class AudioDAL:
    """Data Access layer for operating audio info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_audio(
            self, user_id: uuid.UUID,
            data: bytes
    ) -> AudioFile:
        """
        Создание аудио файла в бд
        :param user_id: UUID пользователя
        :param data: файл в двоичном виде
        :return: AudioFile
        """
        new_audiofile = AudioFile(
            user_id=user_id,
            data=data
        )

        self.db_session.add(new_audiofile)
        await self.db_session.flush()

        return new_audiofile

    async def get_by_user_audio_file(
            self, user_id: uuid.UUID,
            file_id: uuid.UUID
    ) -> AudioFile | None:
        """
        Получение всех аудио файлов текущего пользователя
        :param user_id: UUID текущего пользователя
        :param file_id: UUID file
        :return: список с аудиофайлами
        """
        query = select(AudioFile).where(and_(AudioFile.user == user_id,
                                             AudioFile.id == file_id))

        result = await self.db_session.execute(query)
        all_audio_files = result.fetchone()

        if all_audio_files is not None:
            return all_audio_files[0]



