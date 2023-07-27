from datetime import datetime, timedelta
from typing import Union, Any, Optional

from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from pydantic import ValidationError

from app.database import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES,\
    JWT_SECRET_KEY, User
from app.utils import AuthUser
from app.internal import TokenPayload
from app.repositories.auth import UserRepository


class AuthenticateUser:

    @AuthUser()
    async def authenticate(self, **kwargs) -> User | None:
        return kwargs.get('user')


class Token:

    def __init__(self, subject: Union[str, Any],
                 expires_delta: Optional[timedelta] = None) -> None:
        self.subject = subject
        self.expires_delta = expires_delta
        self.expire = None

    def create_access_token(self) -> str:

        if self.expires_delta:
            self.expire = datetime.utcnow() + self.expires_delta
        else:
            self.expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = dict(exp=self.expire, sub=str(self.subject))

        return jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


async def current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        token_payload = TokenPayload(**payload)

        if datetime.fromtimestamp(token_payload.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await UserRepository().get_one(email=token_payload.sub)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user

