from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.value import Value
from app.schemas.value import ValueCreate, ValueUpdate


class CRUDValue(CRUDBase[Value, ValueCreate, ValueUpdate]):

    def create_with_recording(self, db_session: Session, obj_in: ValueCreate, recording_id: int) -> Value:
        obj_in_data = jsonable_encoder(obj_in)
        fresh_value = self.model(**obj_in_data, recording_id=recording_id)
        db_session.add(fresh_value)
        db_session.commit()
        db_session.refresh(fresh_value)
        return fresh_value


value = CRUDValue(Value)
