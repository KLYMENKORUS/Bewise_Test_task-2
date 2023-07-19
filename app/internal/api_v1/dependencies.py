from app.services.audio import AudioService
from app.repositories.audio import AudioRepository


def audio_service():
    return AudioService(AudioRepository)