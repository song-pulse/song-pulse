from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.playlist import Playlist
from app.schemas.playlist import PlaylistCreate, PlaylistUpdate


class CRUDPlaylist(CRUDBase[Playlist, PlaylistCreate, PlaylistUpdate]):

    def create_with_participant(self, db_session: Session, obj_in: PlaylistCreate, participant_id: int) -> Playlist:
        obj_in_data = jsonable_encoder(obj_in)
        fresh_playlist = self.model(**obj_in_data, participant_id=participant_id)
        db_session.add(fresh_playlist)
        db_session.commit()
        db_session.refresh(fresh_playlist)
        return fresh_playlist


playlist = CRUDPlaylist(Playlist)
