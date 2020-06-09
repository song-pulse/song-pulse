from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.base_class import Base


class Participant(Base):
    __tablename__ = "participant"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    recordings = relationship("Recording", cascade="all,delete")
    playlists = relationship("Playlist", cascade="all,delete")
    baselines = relationship("Baseline", cascade="all,delete")
