from typing import Annotated

from fastapi import APIRouter, Depends

from app.internal import UserCreate, UserRead
from app.services.auth import UserService
from app.internal import user_service


router = APIRouter(prefix='user', tags=['user'])


@router.post('/register', summary='Create a new user', response_model=UserRead)
async def register(
        body: UserCreate,
        service: Annotated[UserService, Depends(user_service)]
) -> UserRead:

    user = await service.create_user(**body.model_dump())

    return UserRead(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        is_verified=user.is_verified,
    )