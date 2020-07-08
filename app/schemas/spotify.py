from pydantic import BaseModel


class SpotifyBase(BaseModel):
    id: str
    refresh_token: str
    pass


class SpotifyCreate(SpotifyBase):
    pass


class SpotifyUpdate(SpotifyBase):
    pass


class SpotifyInDBBase(SpotifyBase):
    class Config:
        orm_mode = True


# Properties to return to client
class Spotify(SpotifyInDBBase):
    pass


# Properties properties stored in DB
class SpotifyInDB(SpotifyInDBBase):
    pass
