from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from backend.app import CRUDBase
from backend.app.models import Run
from backend.app import RunCreate, RunUpdate


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

    def get_first_for_recording(self, db_session: Session, recording_id: int) -> Run:
        return db_session.query(self.model).filter(self.model.recording_id == recording_id).first()


run = CRUDRun(Run)
