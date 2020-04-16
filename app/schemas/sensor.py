from pydantic import BaseModel


class SensorBase(BaseModel):
    name: str


class SensorCreate(SensorBase):
    pass


class SensorUpdate(SensorBase):
    pass


class SensorInDBBase(SensorBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Sensor(SensorInDBBase):
    pass


# Properties properties stored in DB
class SensorInDB(SensorInDBBase):
    pass
