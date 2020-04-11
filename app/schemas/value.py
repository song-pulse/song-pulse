from pydantic import BaseModel


class ValueBase(BaseModel):
    timestamp: int
    value: int


class ValueCreate(ValueBase):
    pass


class ValueUpdate(ValueBase):
    pass


class ValueInDBBase(ValueBase):
    id: int
    file_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Value(ValueInDBBase):
    pass


# Properties properties stored in DB
class ValueInDB(ValueInDBBase):
    pass
