from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.qtable import QTable
from app.schemas.qtable import QTableCreate, QTableUpdate


class CRUDQTable(CRUDBase[QTable, QTableCreate, QTableUpdate]):

    def create_with_participant(self, db_session: Session, obj_in: QTableCreate, participant_id: int) -> QTable:
        obj_in_data = jsonable_encoder(obj_in)
        fresh_qtable = self.model(**obj_in_data, participant_id=participant_id)
        db_session.add(fresh_qtable)
        db_session.commit()
        db_session.refresh(fresh_qtable)
        return fresh_qtable

    def get_by_participant(self, db_session: Session, participant_id: int) -> QTable:
        return db_session.query(self.model).filter(self.model.participant_id == participant_id).first()


qtable = CRUDQTable(QTable)
