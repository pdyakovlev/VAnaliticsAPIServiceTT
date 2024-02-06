from sqlalchemy import Column, ForeignKey

from app.core.db import Base

from sqlalchemy import Table


association_table = Table(
    "pipeline_step",
    Base.metadata,
    Column('pipeline_id', ForeignKey('pipeline.id'), primary_key=True),
    Column('step_id', ForeignKey('step.id'), primary_key=True),
)
