from fastapi import HTTPException, status

from app.utils import AbstractRepository, UserAlreadyExists
from app.utils.hashing import Hasher
from app.database import User


class UserService:

    def __init__(self, repository: AbstractRepository):
        self.repository: AbstractRepository = repository()

    @UserAlreadyExists()
    async def create_user(self, **kwargs) -> User:
        return await self.repository.add_one(
            username=kwargs.get('username'),
            email=kwargs.get('email'),
            hashed_password=Hasher.get_hashed_pass(kwargs.get('password')),
            is_active=kwargs.get('is_active'),
            is_superuser=kwargs.get('is_superuser'),
            is_verified=kwargs.get('is_verified'),
        )

    async def get_user(self, email: str) -> User | None:
        user = await self.repository.get_one(email=email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not find user",
            )

        return user