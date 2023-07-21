import uuid
from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr, BaseModel, Field


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


class AudioSchemas(BaseModel):
    id: uuid.UUID = Field(..., examples=['bb88fb2a-f20d-4ca7-848d-ecc83498b094'])
    name_file: str = Field(..., examples=['simple_6s'])
    user: EmailStr = Field(..., examples=['user@example.com'])
