from typing import List

from sqlalchemy import Column, String, Text
from sqlalchemy.orm import Mapped, relationship

from app.core.db import Base
from app.models.pipeline_step import association_table


class Pipeline(Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    steps: Mapped[List["Step"]] = relationship(
        secondary=association_table,
        back_populates="pipelines",
        lazy="selectin"
    )
