from datetime import datetime

from beanie import Document, Link
from models.user.user_internal import UserInternal


class BookingsInternal(Document):
    user_id: Link[UserInternal]
    description: str = None
    venue: str = None
    created_at: datetime = datetime.now()

    def __str__(self):
        return f"Booking by : {self.user_id}, created_at: {self.created_at}"

    class Settings:
        name = "bookings"

