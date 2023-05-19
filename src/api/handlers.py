import io
import typing
import uuid
from fastapi import APIRouter, Depends, HTTPException, File
from sqlalchemy.exc import IntegrityError
from starlette import status
from fastapi.responses import Response

from api.utils import current_user, AudioService
from db.models import User
from api.schemas import ResponseCreateAudioUrl
from config.settings import DB_PORT

router = APIRouter(prefix='/audio', tags=['music'])


@router.post(
    '/add',
    response_model=ResponseCreateAudioUrl,
    summary='Загрузка аудиофайла'
)
async def add_audio_file(
        audio_file: typing.Annotated[bytes, File(...)],
        user: User = Depends(current_user),
        service: AudioService = Depends()
) -> ResponseCreateAudioUrl:
    """
    Хендлер создания аудиофайла:
        - Конвертирует файл из wav в mp3
        - Создаем запись в бд
        - Возвращаем ссылку для скачивания
    """
    try:
        audio = await service.create_audio(audio_file, user.id)
        url = f'http://127.0.0.1:{DB_PORT}/record?id={audio.id}&user={audio.user}'
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Аудиозапись с таким названием существует')

    return ResponseCreateAudioUrl(
        url=url
    )


@router.get(
    '/record',
    summary='Скачивание аудиофайла'
)
async def download_audio_file(
        file_id: uuid.UUID,
        user: User = Depends(current_user),
        service: AudioService = Depends()
) -> Response:
    """
    Хендлер для скачивания файла
        - Ищет файл по id пользователя и id файла
    :param file_id: file id
    :param user: current user
    :param service: audio service
    """
    audio_file_mp3 = await service.get_by_user_audio_file(
        user_id=user.id,
        file_id=file_id
    )
    if audio_file_mp3 is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='File not found'
        )
    content_type = io.BytesIO(audio_file_mp3).read()
    return Response(
        content=content_type,
        media_type='audio/mpeg',
        headers={'Content-Disposition': f'attachment; filename="{audio_file_mp3.id}"'}
    )
