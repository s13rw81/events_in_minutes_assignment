from typing import Annotated

from api.user.request_models.register_request_model import Register
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from logging_config import log
from logic.user.authentication import authenticate_user
from logic.user.token import create_access_token
from models.user.user_external import UserExternal
from models.user.user_internal import UserInternal
from data.generic_models.response_model import SuccessResponse
from pymongo.errors import DuplicateKeyError
from starlette import status
from utils.password_utils import generate_password_hash

user_api_router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@user_api_router.post("/register")
async def register(register_user: Register):
    log.info(f"/register invoked: register_user = {register_user}")

    user = UserInternal(
        name=register_user.name,
        email=register_user.email,
        username=register_user.username,
        password=generate_password_hash(register_user.password),
    )
    try:
        result = await user.insert()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="could not save the user in the database"
            )
    except DuplicateKeyError as e:
        raise HTTPException(status_code=400, detail="Username or email already exists.") from e
    return SuccessResponse(status_code=status.HTTP_201_CREATED, detail="user created successfully.", data=str(result))


@user_api_router.get("/all-users")
async def get_all_users():
    result = await UserExternal.find({}).to_list()
    return SuccessResponse(status_code=status.HTTP_200_OK, detail='OK', data=result)


@user_api_router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> SuccessResponse:
    log.info(f"inside auth/token username={form_data.username}")

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    user = await authenticate_user(username=form_data.username, plain_password=form_data.password)

    if not user:
        raise credentials_exception

    access_token = await create_access_token(data={"sub": user.email_address if user.email_address else user.phone_number})
    retval = SuccessResponse(status_code=status.HTTP_200_OK, data=access_token, detail="Bearer")
    log.info(f"returning {retval}")

    return retval
