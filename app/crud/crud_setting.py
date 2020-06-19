from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.setting import Setting
from app.schemas.setting import SettingCreate, SettingUpdate


class CRUDSetting(CRUDBase[Setting, SettingCreate, SettingUpdate]):

    def create(self, db_session: Session, obj_in: SettingCreate) -> Setting:
        obj_in_data = jsonable_encoder(obj_in)
        fresh_setting = self.model(**obj_in_data)
        db_session.add(fresh_setting)
        db_session.commit()
        db_session.refresh(fresh_setting)
        return fresh_setting

    def get(self, db_session: Session, id: int = 1) -> Setting:
        return db_session.query(self.model).filter(self.model.id == id).first()


setting = CRUDSetting(Setting)
