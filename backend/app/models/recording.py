from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from backend.app.database.base_class import Base


class Recording(Base):
    __tablename__ = "recording"

    id = Column(Integer, primary_key=True, index=True)
    participant_id = Column(Integer, ForeignKey("participant.id"))
    name = Column(String)

    files = relationship("File", cascade="all,delete")
    runs = relationship("Run", cascade="all,delete")
