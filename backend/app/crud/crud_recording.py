from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from backend.app import CRUDBase
from backend.app.models import Recording
from backend.app import RecordingCreate, RecordingUpdate


class CRUDRecording(CRUDBase[Recording, RecordingCreate, RecordingUpdate]):

    def create_with_participant(self, db_session: Session, obj_in: RecordingCreate, participant_id: int) -> Recording:
        obj_in_data = jsonable_encoder(obj_in)
        fresh_recording = self.model(**obj_in_data, participant_id=participant_id)
        db_session.add(fresh_recording)
        db_session.commit()
        db_session.refresh(fresh_recording)
        return fresh_recording

    def get_by_participant(self, db_session: Session, participant_id: int, skip=0, limit=100) -> List[Recording]:
        return db_session.query(self.model).filter(self.model.participant_id == participant_id).offset(skip).limit(limit).all()


recording = CRUDRecording(Recording)
