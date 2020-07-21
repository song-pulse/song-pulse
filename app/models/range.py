from sqlalchemy import Column, ForeignKey, Integer, String, Float

from app.database.base_class import Base


class Range(Base):
    __tablename__ = "range"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("run.id"))
    name = Column(String)
    min = Column(Float)
    max = Column(Float)
    counter = Column(Integer)
