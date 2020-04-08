from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.participant import Participant
from app.schemas.participant import ParticipantCreate, ParticipantUpdate


class CRUDParticipant(CRUDBase[Participant, ParticipantCreate, ParticipantUpdate]):

    def create(self, db_session: Session, obj_in: ParticipantCreate) -> Participant: # TODO: this is the base implementation use that
        obj_in_data = jsonable_encoder(obj_in)
        fresh_participant = self.model(**obj_in_data)
        db_session.add(fresh_participant)
        db_session.commit()
        db_session.refresh(fresh_participant)
        return fresh_participant


participant = CRUDParticipant(Participant)
