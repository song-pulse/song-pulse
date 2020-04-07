from pydantic import BaseModel


class ValueBase(BaseModel):
    type: int
    timestamp: int
    value: int


class ValueCreate(ValueBase):
    pass


class ValueUpdate(ValueBase):
    pass


class ValueInDBBase(ValueBase):
    id: int
    recording_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Value(ValueInDBBase):
    pass


# Properties properties stored in DB
class ValueInDB(ValueInDBBase):
    pass
