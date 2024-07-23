from typing import Annotated

from data.generic_models.response_model import SuccessResponse
from fastapi import APIRouter, Depends, HTTPException
from logging_config import log
from logic.user.token import get_user_from_token
from models.bookings.bookings_internal import BookingsInternal
from models.user.user_internal import UserInternal
from pymongo.errors import DuplicateKeyError
from starlette import status

bookings_api_router = APIRouter(
    prefix = "/bookings",
    tags = ["bookings"]
)


@bookings_api_router.post("/create")
async def create_new_booking(new_booking, user: Annotated[UserInternal, Depends(get_user_from_token)]):
    log.info(f"/create invoked: new_booking = {new_booking} by user {user}")

    new_booking = BookingsInternal(
        user_id = user.id,
        descripton = new_booking.descripton,
        venue = new_booking.venue,
    )
    try:
        result = await new_booking.insert()
        if not result:
            raise HTTPException(
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail = "could not save the user in the database"
            )
    except DuplicateKeyError as e:
        raise HTTPException(status_code = 400, detail = "Username or email already exists.") from e

    return SuccessResponse(status_code = status.HTTP_201_CREATED, detail = "booking created successfully.",
                           data = str(result))
