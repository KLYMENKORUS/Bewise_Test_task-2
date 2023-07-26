from app.database import User
from app.utils import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User
