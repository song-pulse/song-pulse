from pydantic import BaseModel


class TendencyBase(BaseModel):
    timestamp: int
    eda: int
    mean_rr: int
    prr_20: int


class TendencyCreate(TendencyBase):
    pass


class TendencyUpdate(TendencyBase):
    pass


class TendencyInDBBase(TendencyBase):
    id: int
    run_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Tendency(TendencyInDBBase):
    pass


# Properties properties stored in DB
class TendencyInDB(TendencyInDBBase):
    pass
