from typing import Any

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    code: str = Field(..., examples=["bad_request"])
    message: str = Field(..., examples=["from must be lower or equal to to"])
    details: Any | None = Field(default=None)
    request_id: str = Field(..., examples=["7d5f7f0a-7e65-4c9d-b6d8-9e52d0c8d3e1"])
