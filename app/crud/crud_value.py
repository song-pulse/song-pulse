from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.value import Value
from app.schemas.value import ValueCreate, ValueUpdate


class CRUDValue(CRUDBase[Value, ValueCreate, ValueUpdate]):

    def create_with_file(self, db_session: Session, obj_in: ValueCreate, file_id: int) -> Value:
        obj_in_data = jsonable_encoder(obj_in)
        fresh_value = self.model(**obj_in_data, file_id=file_id)
        db_session.add(fresh_value)
        db_session.commit()
        db_session.refresh(fresh_value)
        return fresh_value

    def get_all_for_file(self, db_session: Session, file_id: int) -> Value:
        return db_session.query(self.model).filter(self.model.file_id == file_id).all()

    def get_prev(self, db_session: Session, file_id: int, timestamp: int, limit: int = 2) -> List[Value]:
        return db_session.query(self.model).filter(self.model.file_id == file_id) \
            .filter(self.model.timestamp < timestamp) \
            .order_by(self.model.timestamp.desc()).limit(limit).all()


value = CRUDValue(Value)
