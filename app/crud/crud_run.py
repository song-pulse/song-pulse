from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.run import Run
from app.schemas.run import RunCreate, RunUpdate


class CRUDRun(CRUDBase[Run, RunCreate, RunUpdate]):

    def create_with_recoding(self, db_session: Session, obj_in: RunCreate, recording_id: int) -> Run:
        obj_in_data = jsonable_encoder(obj_in)
        fresh_run = self.model(**obj_in_data, recording_id=recording_id)
        db_session.add(fresh_run)
        db_session.commit()
        db_session.refresh(fresh_run)
        return fresh_run

    def get_all_for_recording(self, db_session: Session, recording_id: int) -> List[Run]:
        return db_session.query(self.model).filter(self.model.recording_id == recording_id).all()


run = CRUDRun(Run)
