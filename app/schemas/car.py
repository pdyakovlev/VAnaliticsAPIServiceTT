from typing import Optional

from pydantic import BaseModel, Field


class CarSchema(BaseModel):

    id: int
    is_detected: bool = Field
    coordinates: Optional[str] = Field

    class Config:
        from_attributes = True
