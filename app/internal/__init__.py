from .api_v1.schemas import UserRead, UserCreate, TokenSchemas, TokenPayload
from .api_v1.handlers import router as router_handlers
from .api_v1.handlers import add_music, all_audio_by_user, download_audio_file, delete_audio
from .pages.router import router as router_pages
from .api_v1.dependencies import user_service, auth_service