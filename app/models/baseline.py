from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base_class import Base


class Baseline(Base):
    __tablename__ = "baseline"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensor.id"))
    participant_id = Column(Integer, ForeignKey("participant.id"))
    baseline = Column(Float)
    counter = Column(Integer)
    max_value = Column(Float)
    min_value = Column(Float)

    sensor = relationship("Sensor")
