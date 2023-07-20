import io
from functools import wraps

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

from app.repositories.audio import AudioRepository


class AudioException:

    def __init__(self, message: str):
        self.message = message

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=self.message
                )
        return wrapper


class AudioDoesNotExist:

    def __init__(self, message: str):
        self.message = message
        self.audio_service = AudioRepository()

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):

            audio_file = await self.audio_service.get_one(
                user=kwargs.get('user'), name_file=kwargs.get('name_file')
            )

            if audio_file:
                args += (audio_file,)
                return await func(*args, **kwargs)

            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=self.message
                )
        return wrapper


class Convert:

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                audio_wav = AudioSegment.from_wav(io.BytesIO(await kwargs.get('data').read()))
                convert_file = audio_wav.export(format='mp3').read()
                kwargs.update({'data': convert_file})
                return await func(*args, **kwargs)

            except CouldntDecodeError:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f'Wrong file format'
                )
        return wrapper
