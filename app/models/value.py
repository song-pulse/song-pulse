from sqlalchemy import Column, ForeignKey, Integer, Float, BigInteger
from sqlalchemy.orm import relationship

from app.database.base_class import Base


class Value(Base):
    __tablename__ = "value"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("file.id"))
    timestamp = Column(BigInteger)
    value1 = Column(Float)
    value2 = Column(Float)
    value3 = Column(Float)
