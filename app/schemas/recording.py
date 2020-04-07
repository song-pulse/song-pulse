from typing import List

from pydantic import BaseModel

from .run import Run
from .value import Value


class RecordingBase(BaseModel):
    total_time: int


class RecordingCreate(RecordingBase):
    pass


class RecordingUpdate(RecordingBase):
    pass


class RecordingInDBBase(RecordingBase):
    id: int
    participant_id: int

    values: List[Value] = []
    runs: List[Run] = []

    class Config:
        orm_mode = True


# Properties to return to client
class Recording(RecordingInDBBase):
    pass


# Properties properties stored in DB
class RecordingInDB(RecordingInDBBase):
    pass
