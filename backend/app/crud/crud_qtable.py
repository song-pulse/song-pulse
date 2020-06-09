from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from backend.app import CRUDBase
from backend.app.models import QTable
from backend.app.schemas.qtable import QTableCreate, QTableUpdate


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
