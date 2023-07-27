from app.services.audio import AudioService
from app.services.auth.auth import UserService
from app.repositories.audio import AudioRepository
from app.repositories.auth import UserRepository
from app.services.auth.utils import AuthenticateUser


def audio_service():
    return AudioService(AudioRepository)


def user_service():
    return UserService(UserRepository)


def auth_service():
    return AuthenticateUser()