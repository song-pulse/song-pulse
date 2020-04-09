from pydantic import BaseModel

from .sensor import Sensor


class ValueBase(BaseModel):
    sensor_id: int
    timestamp: int
    value: int


class ValueCreate(ValueBase):
    pass


class ValueUpdate(ValueBase):
    pass


class ValueInDBBase(ValueBase):
    id: int
    recording_id: int

    sensor: Sensor

    class Config:
        orm_mode = True


# Properties to return to client
class Value(ValueInDBBase):
    pass


# Properties properties stored in DB
class ValueInDB(ValueInDBBase):
    pass
