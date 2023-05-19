from fastapi import APIRouter
from api.schemas import UserRead, UserCreate
from api.utils import fastapi_users, auth_backend
from api.handlers import router as handlers

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(handlers)