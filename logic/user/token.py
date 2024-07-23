from datetime import timedelta, datetime, timezone
from typing import Annotated, Any, Coroutine

from config import JWT_TOKEN_EXPIRY_IN_DAYS, JWT_SECRET_KEY, JWT_ALGORITHM
from data.dbapi.user.read_queries import get_user_by_email, get_user_by_username
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from logging_config import log
from models.user.user_internal import UserInternal
from starlette import status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "auth/token")


async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    log.info(f"create_access_token invoked: data={data}")
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days = JWT_TOKEN_EXPIRY_IN_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm = JWT_ALGORITHM)
    log.info(f"returning {encoded_jwt}")
    return encoded_jwt


async def get_user_from_token(token: Annotated[str, Depends(oauth2_scheme)]) -> Coroutine[Any, Any, Any]:
    log.info(f"get_current_user invoked: token={token}")

    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms = [JWT_ALGORITHM])
        sub: str = payload.get("sub")

        if sub is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user_by_email = get_user_by_email(email = sub)
    user_by_username = get_user_by_username(username = sub)
    user = user_by_email or user_by_username
    log.info(f"returning {user}")

    return user
