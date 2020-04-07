from pydantic import BaseModel


class ResultBase(BaseModel):
    timestamp: int
    song: str
    verdict: int


class ResultCreate(ResultBase):
    pass


class ResultUpdate(ResultBase):
    pass


class ResultInDBBase(ResultBase):
    id: int
    run_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Result(ResultInDBBase):
    pass


# Properties properties stored in DB
class ResultInDB(ResultInDBBase):
    pass
