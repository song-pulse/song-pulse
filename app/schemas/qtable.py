from pydantic import BaseModel


class QTableBase(BaseModel):
    data: str


class QTableCreate(QTableBase):
    pass


class QTableUpdate(QTableBase):
    pass


class QTableInDBBase(QTableBase):
    id: int
    participant_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class QTable(QTableInDBBase):
    pass


# Properties properties stored in DB
class QTableInDB(QTableInDBBase):
    pass
