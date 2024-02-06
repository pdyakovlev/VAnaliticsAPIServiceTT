from typing import Optional

from pydantic import BaseModel, Field, validator


class PipelineBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]


class PipelineCreate(PipelineBase):
    name: str = Field(..., min_length=1, max_length=100)


class PipelineDB(PipelineCreate):
    id: int

    class Config:
        from_attributes = True


class PipelineUpdate(PipelineBase):
    @validator('name')
    def name_is_not_null(cls, value):
        if value is None:
            raise ValueError("Имя не может быть пустым.")
        return value
