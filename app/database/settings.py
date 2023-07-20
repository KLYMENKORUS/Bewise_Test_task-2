from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: str

    class Config:
        env_file = '.env'


@lru_cache()
def get_settings():
    data = Settings()

    return {
        'db_user': data.POSTGRES_USER,
        'db_pass': data.POSTGRES_PASSWORD,
        'db_name': data.POSTGRES_DB,
        'db_port': data.POSTGRES_PORT,
    }


settings = get_settings()

db_url = f'postgresql+asyncpg://{settings.get("db_user")}:' \
         f'{settings.get("db_pass")}@127.0.0.1:{settings.get("db_port")}/{settings.get("db_name")}'

