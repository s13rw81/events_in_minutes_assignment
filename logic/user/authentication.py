from data.dbapi.user.read_queries import get_user_by_email, get_user_by_username
from logging_config import log
from models.user.user_internal import UserInternal
from utils.password_utils import verify_password


async def authenticate_user(username: str, plain_password: str) -> UserInternal | None:
    log.info(f"authenticate_user invoked: username={username}")

    user_from_email = await get_user_by_email(email=username)
    user_from_username = await get_user_by_username(username=username)
    log.info(f"user_from_email: {user_from_email}, user_from_username : {user_from_username}")

    user = user_from_email or user_from_username

    if user is None:
        return None

    is_verified = verify_password(plain_password=plain_password, hashed_password=user.password)
    log.info(f"password verified for {user} = {is_verified}")
    retval = user if is_verified else None
    log.info(f"returning authenticated user {retval}")
    return retval
