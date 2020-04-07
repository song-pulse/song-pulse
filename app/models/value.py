from sqlalchemy import Column, ForeignKey, Integer, Float, BigInteger

from app.database.base_class import Base


class Value(Base):
    __tablename__ = "values"

    id = Column(Integer, primary_key=True, index=True)
    recording_id = Column(Integer, ForeignKey("recordings.id"), index=True)
    type = Column(Integer, index=True)
    timestamp = Column(BigInteger, index=True)
    value = Column(Float)
