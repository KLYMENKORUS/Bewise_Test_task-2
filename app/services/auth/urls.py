from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.internal import UserCreate, UserRead, TokenSchemas
from app.services.auth.auth import UserService
from app.internal import user_service, auth_service
from app.database import ACCESS_TOKEN_EXPIRE_MINUTES
from .utils import AuthenticateUser, Token


router = APIRouter(prefix='/user', tags=['user'])


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


@router.post('/login', summary='Create access token for user', response_model=TokenSchemas)
async def login(
        auth: Annotated[AuthenticateUser, Depends(auth_service)],
        form_data: OAuth2PasswordRequestForm = Depends()
) -> TokenSchemas:
    user = await auth.authenticate(email=form_data.username, password=form_data.password)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = Token(user.email, access_token_expires).create_access_token()

    return TokenSchemas(
        access_token=access_token,
        token_type='Bearer'
    )

