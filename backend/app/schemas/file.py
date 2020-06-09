from typing import List
from pydantic import BaseModel

from .sensor import Sensor
from .value import Value


class FileBase(BaseModel):
    sensor_id: int
    name: str


class FileCreate(FileBase):
    pass


class FileUpdate(FileBase):
    pass


class FileInDBBase(FileBase):
    id: int
    recording_id: int

    sensor: Sensor
    values: List[Value] = []

    class Config:
        orm_mode = True


# Properties to return to client
class File(FileInDBBase):
    pass


# Properties properties stored in DB
class FileInDB(FileInDBBase):
    pass
