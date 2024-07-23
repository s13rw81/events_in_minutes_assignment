from api.user.request_models.register_request_model import Register
from data.generic_models.response_model import SuccessResponse
from fastapi import APIRouter, HTTPException
from logging_config import log
from models.user.user_external import UserExternal
from models.user.user_internal import UserInternal
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


