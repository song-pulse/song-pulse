from sqlalchemy import Column, Integer, String, ForeignKey

from app.database.base_class import Base


class QTable(Base):
    __tablename__ = "qtable"

    id = Column(Integer, primary_key=True, index=True)
    participant_id = Column(Integer, ForeignKey("participant.id"), index=True)
    data = Column(String)
