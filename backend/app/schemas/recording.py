from typing import List

from pydantic import BaseModel

from .run import Run
from .file import File


class RecordingBase(BaseModel):
    name: str


class RecordingCreate(RecordingBase):
    pass


class RecordingUpdate(RecordingBase):
    pass


class RecordingInDBBase(RecordingBase):
    id: int
    participant_id: int

    files: List[File] = []
    runs: List[Run] = []

    class Config:
        orm_mode = True


# Properties to return to client
class Recording(RecordingInDBBase):
    pass


# Properties properties stored in DB
class RecordingInDB(RecordingInDBBase):
    pass
