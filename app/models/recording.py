from sqlalchemy import Column, Integer, BigInteger
from sqlalchemy.orm import relationship

from app.database.base_class import Base


class Recording(Base):
    __tablename__ = "recordings"

    id = Column(Integer, primary_key=True, index=True)
    participant_id = Column(Integer, index=True)
    total_time = Column(BigInteger, index=True)

    values = relationship("Value")
    runs = relationship("Run")
