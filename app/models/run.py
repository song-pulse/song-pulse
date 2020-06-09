from sqlalchemy import Column, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship

from app.database.base_class import Base


class Run(Base):
    __tablename__ = "run"

    id = Column(Integer, primary_key=True, index=True)
    recording_id = Column(Integer, ForeignKey("recording.id"))
    is_running = Column(Boolean)

    results = relationship("Result", cascade="all,delete")
