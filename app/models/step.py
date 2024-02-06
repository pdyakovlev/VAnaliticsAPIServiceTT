from typing import List

from sqlalchemy import Column, String, Text
from sqlalchemy.orm import Mapped, relationship

from app.core.db import Base
from app.models.pipeline_step import association_table


class Step(Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    pipelines: Mapped[List["Pipeline"]] = relationship(
        secondary=association_table,
        back_populates="steps",
        lazy='selectin'
    )
    func = Column(String(100))
