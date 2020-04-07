from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.recording import Recording
from app.schemas.recording import RecordingCreate, RecordingUpdate


class CRUDRecording(CRUDBase[Recording, RecordingCreate, RecordingUpdate]):

    def create_with_participant(self, db_session: Session, obj_in: RecordingCreate, participant_id: str) -> Recording:
        obj_in_data = jsonable_encoder(obj_in)
        fresh_recording = self.model(**obj_in_data, participant_id=participant_id)
        db_session.add(fresh_recording)
        db_session.commit()
        db_session.refresh(fresh_recording)
        return fresh_recording


recording = CRUDRecording(Recording)
