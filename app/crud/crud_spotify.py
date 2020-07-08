from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.spotify import Spotify
from app.schemas.spotify import SpotifyCreate, SpotifyUpdate


class CRUDSpotify(CRUDBase[Spotify, SpotifyCreate, SpotifyUpdate]):

    def create(self, db_session: Session,
               obj_in: SpotifyCreate) -> Spotify:  # TODO: this is the base implementation use that
        obj_in_data = jsonable_encoder(obj_in)
        fresh_spotify = self.model(**obj_in_data)
        db_session.add(fresh_spotify)
        db_session.commit()
        db_session.refresh(fresh_spotify)
        return fresh_spotify


spotify = CRUDSpotify(Spotify)
