from sqlalchemy import Column, ForeignKey, Integer, Float, BigInteger
from sqlalchemy.orm import relationship

from app.database.base_class import Base


class Value(Base):
    __tablename__ = "value"

    id = Column(Integer, primary_key=True, index=True)
    recording_id = Column(Integer, ForeignKey("recording.id"))
    sensor_id = Column(Integer, ForeignKey("sensor.id"))
    timestamp = Column(BigInteger)
    value = Column(Float)

    sensor = relationship("Sensor")
