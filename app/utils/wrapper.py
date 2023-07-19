import io
from functools import wraps

from fastapi import HTTPException, status
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError


class DatabaseSession:

    def __init__(self, db_session):
        self.db_session = db_session

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            async with self.db_session() as session:
                async with session.begin():
                    return await func(*args, session, **kwargs)

        return wrapper


class Convert:

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                audio_wav = AudioSegment.from_wav(kwargs.get('data').file)
                convert_file = audio_wav.export(kwargs.get('data').filename, format='mp3')
                kwargs.update({'data': convert_file.read()})

                return await func(*args, **kwargs)

            except CouldntDecodeError:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f'Wrong file format'
                )
        return wrapper
