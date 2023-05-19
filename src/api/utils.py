import io
import os
import uuid
from fastapi import Depends, HTTPException, status
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy
from sqlalchemy.ext.asyncio import AsyncSession
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from db.manager import get_user_manager
from db.models import User, AudioFile
from db.session import get_db
from api.optional import AudioAction, UserAction


# backend get_jwt_strategy
cookie_transport = CookieTransport(cookie_name='auth', cookie_max_age=3600)


SECRET = "SECRET"


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()


# backend AudioService
class AudioService:

    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    def convert_wav_to_mp3(self, file: bytes) -> bytes:
        """
        Конвертация аудиофайла из wav в mp3
        :param file: File to convert
        """
        #ffmpeg_path = os.path.join( 
        #   'static/ffmpeg-6.0-full_build/bin/ffmpeg.exe')
        # AudioSegment.converter = ffmpeg_path # for windows 
        audio_wav = AudioSegment.from_wav(io.BytesIO(file))
        audio_mp3 = io.BytesIO()
        audio_wav.export(audio_mp3, format='mp3')
        return audio_mp3.read()

    async def create_audio(
            self, audio_file: bytes,
            user_id: uuid.UUID
    ) -> AudioFile:
        """
        Создание нового аудио файла
        """
        get_user = UserAction.get_user_by_id(user_id, self.session)
        if get_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User do not exists'
            )
        try:
            file_mp3 = self.convert_wav_to_mp3(audio_file)
            audio = await AudioAction.create_audio(
                user_id=user_id,
                data=file_mp3,
                db_session=self.session
            )
            return audio
        except CouldntDecodeError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f'Wrong file format {e}'
            )

    async def get_by_user_audio_file(
            self, user_id: uuid.UUID,
            file_id: uuid.UUID
    ) -> AudioFile | None:
        """
        Получения всех записей пользователя
        :param user_id: UUID текущего пользователя
        :param file_id: UUID file
        :return: список с аудиофайлами
        """
        audio_file = await AudioAction.get_by_user_audio_file(
            user_id=user_id,
            file_id=file_id,
            db_session=self.session
        )
        return audio_file



