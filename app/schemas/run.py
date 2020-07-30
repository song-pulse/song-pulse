from typing import List

from pydantic import BaseModel

from .range import Range
from .result import Result
from .tendency import Tendency


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
    range: List[Range] = []
    tendencies: List[Tendency] = []

    class Config:
        orm_mode = True


# Properties to return to client
class Run(RunInDBBase):
    pass


# Properties properties stored in DB
class RunInDB(RunInDBBase):
    pass
