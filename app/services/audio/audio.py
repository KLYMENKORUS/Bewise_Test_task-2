from app.utils import AbstractRepository
from app.utils import Convert, AudioException, AudioDoesNotExist


class AudioService:

    def __init__(self, audio_repo: AbstractRepository):
        self.audio_repo = audio_repo()

    @AudioException('Audio with this title already exists')
    @Convert()
    async def add_audio(self, **kwargs):
        return await self.audio_repo.add_one(
            user=kwargs.get('user'),
            data=kwargs.get('data'),
            name_file=kwargs.get('name_file').split('.')[0]
        )

    @AudioDoesNotExist('Audio with given name does not exist')
    async def get_audio(self, *args, **kwargs):
        return args

    async def get_all_by_filter(self, *args, **kwargs):
        return await self.audio_repo.get_all_by_filter(user=kwargs.get('user'))