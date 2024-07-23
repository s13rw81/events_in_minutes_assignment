from logging_config import log
from models.user.user_internal import UserInternal


async def get_user_by_email(email: str):
    log.info(f'get user by email {email}')
    res = await UserInternal.find({'email': email}).first_or_none()
    log.info(f'user found : {res}')
    return res


async def get_user_by_username(username: str):
    log.info(f'get user by username {username}')
    res = await UserInternal.find({'username': username}).first_or_none()
    log.info(f'user found : {res}')
    return res
