from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.app.database.base_class import Base


class File(Base):
    __tablename__ = "file"

    id = Column(Integer, primary_key=True, index=True)
    recording_id = Column(Integer, ForeignKey("recording.id"))
    sensor_id = Column(Integer, ForeignKey("sensor.id"))
    name = Column(String)

    sensor = relationship("Sensor")
    values = relationship("Value", cascade="all,delete")
