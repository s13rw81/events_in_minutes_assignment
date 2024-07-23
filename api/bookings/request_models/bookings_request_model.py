from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BookingsRequest(BaseModel):
    description: Optional[str]
    venue_id: Optional[int] = None
    event_start: Optional[datetime] = None
    event_end: Optional[datetime] = None
    booking_id: Optional[str] = None
