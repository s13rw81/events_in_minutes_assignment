from datetime import datetime
from typing import Optional

import pytz
from beanie import Document, Link
from models.user.user_internal import UserInternal
from pydantic import field_validator, model_validator

utc = pytz.UTC


class BookingsInternal(Document):
    user_id: Link[UserInternal]
    description: Optional[str] = None
    venue_id: Optional[int] = None
    event_start: datetime = None
    event_end: datetime = None
    created_at: datetime = datetime.now(tz = utc)

    @model_validator(mode = 'after')
    def validate_dates(self):
        if not self.event_end >= self.event_start and self.event_start >= self.created_at:
            raise ValueError("Event end cannot be before the event start time.")
        return self

    def __str__(self):
        return f"Booking by : {self.user_id.username}, created_at: {self.created_at}"

    class Settings:
        name = "bookings"
