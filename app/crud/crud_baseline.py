from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.baseline import Baseline
from app.schemas.baseline import BaselineCreate, BaselineUpdate


class CRUDBaseline(CRUDBase[Baseline, BaselineCreate, BaselineUpdate]):

    def create(self, db_session: Session, obj_in: BaselineCreate) -> Baseline:
        obj_in_data = jsonable_encoder(obj_in)
        fresh_baseline = self.model(**obj_in_data)
        db_session.add(fresh_baseline)
        db_session.commit()
        db_session.refresh(fresh_baseline)
        return fresh_baseline


baseline = CRUDBaseline(Baseline)
