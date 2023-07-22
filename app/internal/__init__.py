from .api_v1.schemas import UserRead, UserCreate
from .api_v1.handlers import router as router_handlers
from .api_v1.handlers import add_music, all_audio_by_user
from .pages.router import router as router_pages