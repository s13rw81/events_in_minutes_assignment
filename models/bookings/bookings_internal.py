from datetime import datetime
from typing import Optional

import pytz
from beanie import Document, Link
from data.enums.booking_status import BookingStatus
from models.user.user_internal import UserInternal
from pydantic import model_validator

utc = pytz.UTC


class BookingsInternal(Document):
    user_id: Link[UserInternal]
    description: Optional[str] = None
    venue_id: Optional[int] = None
    event_start: datetime = None
    event_end: datetime = None
    created_at: datetime = datetime.now(tz = utc)
    status: BookingStatus = BookingStatus.ACTIVE

    @model_validator(mode = 'after')
    def validate_dates(cls):
        if not cls.event_end >= cls.event_start and cls.event_start >= cls.created_at:
            raise ValueError("Event end cannot be before the event start time.")
        return cls

    def __str__(self):
        return f"Booking by : {self.user_id}, created_at: {self.created_at}"

    class Settings:
        name = "bookings"
