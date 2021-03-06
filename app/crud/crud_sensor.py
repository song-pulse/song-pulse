from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.sensor import Sensor
from app.schemas.sensor import SensorCreate, SensorUpdate


class CRUDSensor(CRUDBase[Sensor, SensorCreate, SensorUpdate]):

    def create(self, db_session: Session, obj_in: SensorCreate) -> Sensor:
        obj_in_data = jsonable_encoder(obj_in)
        fresh_sensor = self.model(**obj_in_data)
        db_session.add(fresh_sensor)
        db_session.commit()
        db_session.refresh(fresh_sensor)
        return fresh_sensor


sensor = CRUDSensor(Sensor)
