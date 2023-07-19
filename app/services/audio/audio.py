from app.utils import AbstractRepository
from app.utils import Convert


class AudioService:

    def __init__(self, audio_repo: AbstractRepository):
        self.audio_repo = audio_repo()

    @Convert()
    async def add_audio(self, **kwargs):
        return await self.audio_repo.add_one(
            user=kwargs.get('user'),
            data=kwargs.get('data'),
        )

    async def get_audio(self, data: dict):
        return await self.get_audio(**data)