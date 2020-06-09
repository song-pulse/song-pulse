from pydantic import BaseModel


class SongBase(BaseModel):
    name: str
    link: str


class SongCreate(SongBase):
    pass


class SongUpdate(SongBase):
    pass


class SongInDBBase(SongBase):
    id: int
    playlist_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Song(SongInDBBase):
    pass


# Properties properties stored in DB
class SongInDB(SongInDBBase):
    pass
