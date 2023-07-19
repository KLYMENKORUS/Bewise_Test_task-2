import uuid
from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr, BaseModel
from pydantic.networks import AnyHttpUrl


class UserRead(schemas.BaseUser[uuid.UUID]):
    id: uuid.UUID
    username: str
    email: EmailStr
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class ResponseCreateAudioUrl(BaseModel):
    url: AnyHttpUrl
