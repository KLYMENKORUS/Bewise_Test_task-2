from pathlib import Path

import aiofiles
from http import HTTPStatus
from httpx import AsyncClient

BASE_DIR = Path(__file__).parent
AUDIO_FILE = BASE_DIR / 'sample-6s.wav'


async def test_create_user(client: AsyncClient):
    new_user = {
        "email": "user@example.com",
        "password": "12345",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string"
    }
    response = await client.post(url='/auth/register', json=new_user)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['is_active'] is True


async def test_login(client: AsyncClient):
    response = await client.post(url='auth/jwt/login',
                                 data={'username': 'user@example.com', 'password': '12345'})
    assert response.status_code == HTTPStatus.NO_CONTENT