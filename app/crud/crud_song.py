from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.song import Song
from app.schemas.song import SongCreate, SongUpdate


class CRUDSong(CRUDBase[Song, SongCreate, SongUpdate]):

    def create_with_playlist(self, db_session: Session, obj_in: SongCreate, playlist_id: int) -> Song:
        obj_in_data = jsonable_encoder(obj_in)
        fresh_song = self.model(**obj_in_data, playlist_id=playlist_id)
        db_session.add(fresh_song)
        db_session.commit()
        db_session.refresh(fresh_song)
        return fresh_song


song = CRUDSong(Song)
