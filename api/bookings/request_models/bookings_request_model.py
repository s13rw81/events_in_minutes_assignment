from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BookingsRequest(BaseModel):
    description: Optional[str]
    venue: Optional[str]
    created_at: datetime
