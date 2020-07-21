from sqlalchemy import Column, ForeignKey, Integer, BigInteger

from app.database.base_class import Base


class Tendency(Base):
    __tablename__ = "tendency"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("run.id"))
    timestamp = Column(BigInteger)
    eda = Column(Integer)
    mean_rr = Column(Integer)
    prr_20 = Column(Integer)
