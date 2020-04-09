from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger
from sqlalchemy.orm import relationship

from app.database.base_class import Base


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("runs.id"))
    timestamp = Column(BigInteger)
    song_id = Column(Integer, ForeignKey("songs.id"))
    verdict = Column(Integer)

    song = relationship("Song")
