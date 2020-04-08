from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger

from app.database.base_class import Base


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("runs.id"))
    timestamp = Column(BigInteger)
    song = Column(String)
    verdict = Column(Integer)
