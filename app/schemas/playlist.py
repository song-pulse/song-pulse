from typing import List
from pydantic import BaseModel
from .song import Song


class PlaylistBase(BaseModel):
    type: str
    link: str


class PlaylistCreate(PlaylistBase):
    pass


class PlaylistUpdate(PlaylistBase):
    pass


class PlaylistInDBBase(PlaylistBase):
    id: int
    participant_id: int

    songs: List[Song] = []

    class Config:
        orm_mode = True


# Properties to return to client
class Playlist(PlaylistInDBBase):
    pass


# Properties properties stored in DB
class PlaylistInDB(PlaylistInDBBase):
    pass
