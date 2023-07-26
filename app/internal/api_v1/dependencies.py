from app.services.audio import AudioService
from app.services.auth import UserService
from app.repositories.audio import AudioRepository
from app.repositories.auth import UserRepository


def audio_service():
    return AudioService(AudioRepository)


def user_service():
    return UserService(UserRepository)