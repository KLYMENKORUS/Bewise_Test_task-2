from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Depends

from app.internal import add_music, all_audio_by_user


router = APIRouter(prefix='/pages', tags=['Pages'])

template = Jinja2Templates(directory='app/internal/templates')


@router.get('/add_audio')
def home(request: Request, record_all=Depends(all_audio_by_user)):
    return template.TemplateResponse(
        'index.html', {'request': request, 'record_all': record_all}
    )


@router.post('/add_audio')
def add_audio(request: Request, audio_file=Depends(add_music)):
    return template.TemplateResponse(
        'index.html', {'request': request, 'audio': audio_file}
    )

