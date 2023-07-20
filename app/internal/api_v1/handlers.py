import io
from typing import Annotated

from fastapi import APIRouter, Depends, status, File, UploadFile, Response

from app.database import User
from app.services.auth import current_user
from app.services.audio import AudioService
from .dependencies import audio_service

router = APIRouter(prefix='/audio', tags=['music'])


@router.post('/add')
async def add_music(
        user: Annotated[User, Depends(current_user)],
        service: Annotated[AudioService, Depends(audio_service)],
        audio_file: Annotated[UploadFile, File(...)]
):
    await service.add_audio(user=user.id, data=audio_file, name_file=audio_file.filename)

    return {
        'response': status.HTTP_200_OK,
        'message': 'Audio file successfully added in database'
    }


@router.get('/record')
async def download_audio_file(
        filename: str,
        user: Annotated[User, Depends(current_user)],
        service: Annotated[AudioService, Depends(audio_service)],
) -> Response:

    audio_file = await service.get_audio(user=user.id, name_file=filename)

    content_type = io.BytesIO(audio_file[0].data).read()

    return Response(
        content=content_type,
        media_type='audio/mpeg',
        headers={'Content-Disposition': f'attachment; filename="{audio_file[0].name_file}"'}
    )
