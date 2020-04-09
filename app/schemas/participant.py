from typing import List
from pydantic import BaseModel

from .song import Song
from .recording import Recording


class ParticipantBase(BaseModel):
    name: str


class ParticipantCreate(ParticipantBase):
    pass


class ParticipantUpdate(ParticipantBase):
    pass


class ParticipantInDBBase(ParticipantBase):
    id: int

    recordings: List[Recording] = []
    songs: List[Song] = []

    class Config:
        orm_mode = True


# Properties to return to client
class Participant(ParticipantInDBBase):
    pass


# Properties properties stored in DB
class ParticipantInDB(ParticipantInDBBase):
    pass
