from pydantic import BaseModel


class TimestampValuesBase(BaseModel):
    timestamp: int
    eda: float = None
    ibi: float = None
    temp: float = None
    acc_x: float = None
    acc_y: float = None
    acc_z: float = None


class TimestampValuesCreate(TimestampValuesBase):
    pass


# Properties to return to client
class TimestampValues(TimestampValuesBase):
    pass

