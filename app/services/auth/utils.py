from datetime import datetime, timedelta
from typing import Union, Any, Optional

import jwt

from passlib.context import CryptContext

from app.database import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, JWT_SECRET_KEY


class Hasher:

    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def get_hashed_pass(cls, password: str) -> str:
        return cls.password_context.hash(password)

    @classmethod
    def verify_password(cls, password: str, hashed_pass: str) -> bool:
        return cls.password_context.verify(password, hashed_pass)


class Token:

    def __init__(self, subject: Union[str, Any],
                 expires_delta: Optional[timedelta] = None) -> None:
        self.subject = subject
        self.expires_delta = expires_delta
        self.expire = None

    def create_access_token(self) -> str:

        if self.expires_delta is not None:
            self.expire = datetime.utcnow() + self.expires_delta
        else:
            self.expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = dict(exp=self.expire, sub=str(self.subject))

        return jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)

