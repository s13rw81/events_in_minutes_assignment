from models.user.user_internal import UserInternal


async def get_user_by_email(email: str):
    return await UserInternal.find({'email': email}).first_or_none()


async def get_user_by_username(username: str):
    return await UserInternal.find({'username': username}).first_or_none()
