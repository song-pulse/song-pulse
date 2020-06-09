from typing import List

from pydantic import BaseModel

from .result import Result


class RunBase(BaseModel):
    is_running: bool = False


class RunCreate(RunBase):
    pass


class RunUpdate(RunBase):
    pass


class RunInDBBase(RunBase):
    id: int
    recording_id: int

    results: List[Result] = []

    class Config:
        orm_mode = True


# Properties to return to client
class Run(RunInDBBase):
    pass


# Properties properties stored in DB
class RunInDB(RunInDBBase):
    pass
