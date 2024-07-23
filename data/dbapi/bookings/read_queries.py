from bson import ObjectId
from logging_config import log
from models.bookings.bookings_internal import BookingsInternal
from models.user.user_internal import UserInternal


async def get_booking_by_booking_id(booking_id: str):
    log.info(f'fetching booking but booking id {booking_id}')
    res = await BookingsInternal.find({"_id": ObjectId(booking_id)}).first_or_none()
    log.info(f'booking found : {res}')
    return res


async def get_bookings_by_user_id(user: UserInternal):
    log.info(f'fetching bookings for user id {user.id}')
    res = await BookingsInternal.find(BookingsInternal.user_id.id == ObjectId(user.id)).to_list()
    log.info(f'bookings found : {res}')
    return res
