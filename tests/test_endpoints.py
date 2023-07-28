from pathlib import Path

import aiofiles
from http import HTTPStatus
from httpx import AsyncClient

BASE_DIR = Path(__file__).parent
AUDIO_FILE = BASE_DIR / 'sample-6s.wav'


async def test_create_user(client: AsyncClient, create_user_in_database):
    new_user = {
        "email": "user1@example.com",
        "password": "12345",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string"
    }
    response = await client.post(url='user/register', json=new_user)

    assert response.status_code == 200
    assert response.json().get('is_active') is True


async def test_login(client: AsyncClient):
    response = await client.post(url='user/login',
                                 data={'username': 'user1@example.com', 'password': '12345'},
                                 headers={'Content-Type': 'application/x-www-form-urlencoded'})

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in response.json()


async def test_add_file(
        client: AsyncClient, create_user_in_database):
    new_user = {
        "email": "user1@example.com",
        "password": "12345",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string"
    }
    user = await create_user_in_database(**new_user)

    async def upload_file():
        async with aiofiles.open(AUDIO_FILE, 'rb') as file:
            audio_file = await file.read()

        return audio_file

    response = await client.post(
        url=f'audio/add?email={user.email}', files={'audio_file': ('sample-6s.wav', await upload_file())}
    )

    assert response.status_code == HTTPStatus.OK, response.text




