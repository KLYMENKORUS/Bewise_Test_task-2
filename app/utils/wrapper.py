import io
from functools import wraps

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

from app.repositories.audio import AudioRepository
from app.repositories.auth import UserRepository
from .hashing import Hasher


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

    def __init__(self) -> None:
        self.max_file_size = 5

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                if kwargs.get('data').size / 1024 / 1024 < self.max_file_size:
                    audio_wav = AudioSegment.from_wav(io.BytesIO(await kwargs.get('data').read()))
                    convert_file = audio_wav.export(format='mp3').read()
                    kwargs.update({'data': convert_file})
                    return await func(*args, **kwargs)
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Maximum file size exceeded'
                    )

            except CouldntDecodeError:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f'Wrong file format'
                )
        return wrapper


class UserAlreadyExists:

    def __init__(self):
        self.user_service = UserRepository()

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not await self.user_service.get_one(**kwargs):
                return await func(*args, **kwargs)
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'User with this email: {kwargs.get("email")} already exist'
                )

        return wrapper


class AuthUser:

    def __init__(self):
        self.user_service = UserRepository()
        self.exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password'
            )

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = await self.user_service.get_one(**kwargs)

            if user is None:
                raise self.exception

            if not Hasher.verify_password(kwargs.get('password'), user.hashed_password):
                raise self.exception

            kwargs.update(user=user)

            return await func(*args, **kwargs)

        return wrapper





