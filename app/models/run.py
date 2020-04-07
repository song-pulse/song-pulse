from sqlalchemy import Column, ForeignKey, Integer, Boolean, BigInteger
from sqlalchemy.orm import relationship

from app.database.base_class import Base


class Run(Base):
    __tablename__ = "runs"

    id = Column(Integer, primary_key=True, index=True)
    recording_id = Column(Integer, ForeignKey("recordings.id"), index=True)
    current_time = Column(BigInteger)
    is_running = Column(Boolean)

    results = relationship("Result")
