from typing import Annotated

from fastapi import APIRouter, UploadFile, Depends, status

from app.database import User
from app.services.auth import current_user
from app.services.audio import AudioService
from .dependencies import audio_service

router = APIRouter(prefix='/audio', tags=['music'])


@router.post('/add')
async def add_music(
        audio_file: UploadFile,
        user: Annotated[User, Depends(current_user)],
        service: Annotated[AudioService, Depends(audio_service)]
):
    data = {
        'user': user.id,
        'data': audio_file
    }
    await service.add_audio(**data)
    return {
        'response': status.HTTP_200_OK,
        'message': 'Audio file successfully added in database'
    }