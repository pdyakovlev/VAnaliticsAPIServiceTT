from sqlalchemy import Boolean, String, Column

from app.core.db import Base


class Car(Base):
    is_detected = Column(Boolean)
    coordinates = Column(String)
