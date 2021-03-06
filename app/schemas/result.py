from datetime import datetime

from pydantic import BaseModel

from .song import Song


class ResultBase(BaseModel):
    timestamp: int
    song_id: int
    verdict: int
    input: str
    action: int
    song_queued: bool = False
    song_plays_until: datetime = datetime.now()


class ResultCreate(ResultBase):
    pass


class ResultUpdate(ResultBase):
    pass


class ResultInDBBase(ResultBase):
    id: int
    run_id: int

    song: Song

    class Config:
        orm_mode = True


# Properties to return to client
class Result(ResultInDBBase):
    pass


# Properties properties stored in DB
class ResultInDB(ResultInDBBase):
    pass
