from pydantic import BaseModel

from .sensor import Sensor


class BaselineBase(BaseModel):
    sensor_id: int
    participant_id: int
    baseline: float = 0.0
    counter: int = 0


class BaselineCreate(BaselineBase):
    pass


class BaselineUpdate(BaselineBase):
    pass


class BaselineInDBBase(BaselineBase):
    id: int

    sensor: Sensor

    class Config:
        orm_mode = True


# Properties to return to client
class Baseline(BaselineInDBBase):
    pass


# Properties properties stored in DB
class BaselineInDB(BaselineInDBBase):
    pass
