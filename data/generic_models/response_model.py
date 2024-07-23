from typing import Optional, Any

from pydantic import BaseModel


class SuccessResponse(BaseModel):
    status_code: int
    detail: Optional[str]
    data: Optional[Any]


class Token(BaseModel):
    access_token: str
    token_type: str
