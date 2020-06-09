from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger
from sqlalchemy.orm import relationship

from app.database.base_class import Base


class Result(Base):
    __tablename__ = "result"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("run.id"))
    timestamp = Column(BigInteger)
    song_id = Column(Integer, ForeignKey("song.id"))
    verdict = Column(Integer)
    input = Column(String)

    song = relationship("Song")
