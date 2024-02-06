from typing import Optional

from pydantic import BaseModel, Field, validator


class StepBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]
    func: Optional[str]


class StepCreate(StepBase):
    name: str = Field(..., min_length=1, max_length=100)


class StepDB(StepCreate):
    id: int

    class Config:
        from_attributes = True


class StepUpdate(StepBase):
    @validator('name')
    def name_is_not_null(cls, value):
        if value is None:
            raise ValueError("Имя не может быть пустым.")
        return value
