from app.utils import AbstractRepository, UserAlreadyExists
from .utils import Hasher


class UserService:

    def __init__(self, repository: AbstractRepository):
        self.repository: AbstractRepository = repository()

    @UserAlreadyExists()
    async def create_user(self, **kwargs):
        return await self.repository.add_one(
            username=kwargs.get('username'),
            email=kwargs.get('email'),
            password=Hasher.get_hashed_pass(kwargs.get('password')),
            is_active=kwargs.get('is_active'),
            is_superuser=kwargs.get('is_superuser'),
            is_verified=kwargs.get('is_verified'),
        )