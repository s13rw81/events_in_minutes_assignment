from typing import Annotated

from api.bookings.request_models.bookings_request_model import BookingsRequest
from data.dbapi.bookings.read_queries import get_booking_by_booking_id, get_bookings_by_user_id
from data.enums.booking_status import BookingStatus
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


@bookings_api_router.get("/get")
async def get_bookings(user: Annotated[UserInternal, Depends(get_user_from_token)]):
    log.info(f"/get invoked: by user {user}")

    result = await get_bookings_by_user_id(user)
    if not result:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "error occured while fetching bookings of user"
        )

    return SuccessResponse(status_code = status.HTTP_201_CREATED, detail = "booking created successfully.",
                           data = str(result))


@bookings_api_router.post("/create")
async def create_new_booking(new_booking: BookingsRequest, user: Annotated[UserInternal, Depends(get_user_from_token)]):
    log.info(f"/create invoked: new_booking = {new_booking} by user {user}")

    new_booking = BookingsInternal(
        user_id = user.id,
        description = new_booking.description,
        venue_id = new_booking.venue_id,
        event_start = new_booking.event_start,
        event_end = new_booking.event_end

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


@bookings_api_router.put("/update")
async def create_new_booking(update_booking: BookingsRequest,
                             user: Annotated[UserInternal, Depends(get_user_from_token)]):
    log.info(f"/update invoked: update_booking = {update_booking} by user {user}")

    if update_booking.booking_id is None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'booking_id is required')

    existing_booking = await get_booking_by_booking_id(booking_id = update_booking.booking_id)

    if not existing_booking:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'booking with id {update_booking.booking_id} not found')

    # check if user is the creator of booking
    if str(user.id) != existing_booking.user_id.to_dict()['id']:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f'user unauthorised to modify booking')

    update_booking_dict = update_booking.model_dump(exclude_none = True)
    result = await existing_booking.update({"$set": update_booking_dict})
    if not result:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "could not save updates to the booking"
        )

    return SuccessResponse(status_code = status.HTTP_201_CREATED, detail = "booking updated successfully.",
                           data = str(result))


@bookings_api_router.put("/cancel-booking")
async def cancel_booking(booking_id: str, user: Annotated[UserInternal, Depends(get_user_from_token)]):
    log.info(f"/cancel_booking invoked: booking_id = {booking_id} by user {user}")

    if booking_id is None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'booking_id is required')

    existing_booking = await get_booking_by_booking_id(booking_id = booking_id)

    if not existing_booking:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'booking with id {booking_id} not found')

    # check if user is the creator of booking
    if str(user.id) != existing_booking.user_id.to_dict()['id']:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f'user unauthorised to modify booking')

    result = await existing_booking.update({"$set": {'status': BookingStatus.CANCELLED}})
    if not result:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "could not cancel booking"
        )

    return SuccessResponse(status_code = status.HTTP_201_CREATED, detail = "booking cancelled successfully.",
                           data = str(result))
