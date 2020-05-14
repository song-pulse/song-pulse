from sqlalchemy import Column, Float, Integer

from app.database.base_class import Base


class Setting(Base):
    __tablename__ = "setting"

    id = Column(Integer, primary_key=True, index=True)
    stress_threshold = Column(Float)
    acc_threshold = Column(Float)
    eda_threshold = Column(Float)
    ibi_threshold = Column(Float)
    temp_baseline = Column(Float)
    temp_latency = Column(Integer)
    duration = Column(Integer)
