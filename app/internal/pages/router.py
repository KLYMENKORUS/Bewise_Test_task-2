from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Depends

from app.internal import add_music, all_audio_by_user, download_audio_file, \
    delete_audio


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


@router.get('/record')
def record(request: Request, download=Depends(download_audio_file)):
    return template.TemplateResponse(
        'index.html', {'request': request, 'download': download}
    )


@router.delete('/delete')
def delete_audio_file(request: Request, audio_file=Depends(delete_audio)):
    return template.TemplateResponse(
        'index.html', {'request': request, 'audio_file': audio_file}
    )
