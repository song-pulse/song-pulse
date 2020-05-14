from pydantic import BaseModel


class SettingBase(BaseModel):
    stress_threshold: float
    acc_threshold: float
    temp_threshold: float
    eda_threshold: float
    ibi_threshold: float
    temp_latency: int
    duration: int


class SettingCreate(SettingBase):
    pass


class SettingUpdate(SettingBase):
    pass


class SettingInDBBase(SettingBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Setting(SettingInDBBase):
    pass


# Properties properties stored in DB
class SettingInDB(SettingInDBBase):
    pass
