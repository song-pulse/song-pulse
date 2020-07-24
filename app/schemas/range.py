from pydantic import BaseModel


class RangeBase(BaseModel):
    name: str
    min: float = 0.0
    max: float = 0.0
    counter_min: int = 0
    counter_max: int = 0


class RangeCreate(RangeBase):
    pass


class RangeUpdate(RangeBase):
    pass


class RangeInDBBase(RangeBase):
    id: int
    run_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Range(RangeInDBBase):
    pass


# Properties properties stored in DB
class RangeInDB(RangeInDBBase):
    pass
