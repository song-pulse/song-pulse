from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from backend.app import CRUDBase
from backend.app.models import Value
from backend.app.schemas.value import ValueCreate, ValueUpdate


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

value = CRUDValue(Value)
