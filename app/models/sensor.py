from sqlalchemy import Column, Integer, String

from app.database.base_class import Base


class Sensor(Base):
    __tablename__ = "sensor"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    frequency = Column(Integer)
