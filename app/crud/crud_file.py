from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.file import File
from app.schemas.file import FileCreate, FileUpdate


class CRUDFile(CRUDBase[File, FileCreate, FileUpdate]):

    def create_with_recording(self, db_session: Session, obj_in: FileCreate, recording_id: int) -> File:
        obj_in_data = jsonable_encoder(obj_in)
        fresh_value = self.model(**obj_in_data, recording_id=recording_id)
        db_session.add(fresh_value)
        db_session.commit()
        db_session.refresh(fresh_value)
        return fresh_value

    def get_multi_for_recording(self, db_session: Session, recording_id: int) -> List[File]:
        return db_session.query(self.model).filter(self.model.recording_id == recording_id).all()


file = CRUDFile(File)
