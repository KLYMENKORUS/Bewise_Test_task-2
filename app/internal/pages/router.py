from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Depends

from app.internal import add_music


router = APIRouter(prefix='/pages', tags=['Pages'])

template = Jinja2Templates(directory='app/internal/templates')


@router.get('/add')
def home(request: Request):
    return template.TemplateResponse('index.html', {'request': request})


@router.post('/add')
def add_audio(request: Request, audio_file=Depends(add_music)):
    return template.TemplateResponse('index.html', {'request': request, 'audio': audio_file})

