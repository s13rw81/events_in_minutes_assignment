from typing import Annotated

from data.generic_models.response_model import Token
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from logging_config import log
from logic.user.authentication import authenticate_user
from logic.user.token import create_access_token
from starlette import status

auth_api_router = APIRouter(
    prefix = "/auth",
    tags = ["auth"]
)


@auth_api_router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    log.info(f"inside user/token username={form_data.username}")

    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"}
    )

    user = await authenticate_user(username = form_data.username, plain_password = form_data.password)

    if not user:
        raise credentials_exception

    access_token = await create_access_token(data = {"sub": user.email})
    log.info(f'geterated access token for {user}: {access_token}')
    return Token(access_token=access_token, token_type="Bearer")
