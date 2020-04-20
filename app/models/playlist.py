from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base_class import Base


class Playlist(Base):
    __tablename__ = "playlist"

    id = Column(Integer, primary_key=True, index=True)
    participant_id = Column(Integer, ForeignKey("participant.id"), index=True)
    type = Column(String, index=True)
    link = Column(String)

    songs = relationship("Song", cascade="all,delete")
