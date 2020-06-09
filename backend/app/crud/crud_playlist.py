from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from backend.app import CRUDBase
from backend.app.models import Playlist
from backend.app.schemas.playlist import PlaylistCreate, PlaylistUpdate


class CRUDPlaylist(CRUDBase[Playlist, PlaylistCreate, PlaylistUpdate]):

    def create_with_participant(self, db_session: Session, obj_in: PlaylistCreate, participant_id: int) -> Playlist:
        obj_in_data = jsonable_encoder(obj_in)
        fresh_playlist = self.model(**obj_in_data, participant_id=participant_id)
        db_session.add(fresh_playlist)
        db_session.commit()
        db_session.refresh(fresh_playlist)
        return fresh_playlist

    def get_by_participant(self, db_session: Session, participant_id: int, skip=0, limit=100) -> List[Playlist]:
        return db_session.query(self.model).filter(self.model.participant_id == participant_id).offset(skip).limit(limit).all()

    def get_by_participant_and_type(self, db_session: Session, participant_id: int, plist_type: str) -> Playlist:
        return db_session.query(self.model)\
            .filter(self.model.participant_id == participant_id)\
            .filter(self.model.type == plist_type)\
            .first()


playlist = CRUDPlaylist(Playlist)
