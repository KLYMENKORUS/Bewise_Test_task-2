from app.database import AudioFile
from app.utils import SQLAlchemyRepository


class AudioRepository(SQLAlchemyRepository):
    model = AudioFile
