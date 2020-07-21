from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.range import Range
from app.schemas.range import RangeCreate, RangeUpdate


class CRUDRange(CRUDBase[Range, RangeCreate, RangeUpdate]):

    def create_with_run(self, db_session: Session, obj_in: RangeCreate,
                        run_id: int) -> Range:
        obj_in_data = jsonable_encoder(obj_in)
        fresh_range = self.model(**obj_in_data, run_id=run_id)
        db_session.add(fresh_range)
        db_session.commit()
        db_session.refresh(fresh_range)
        return fresh_range

    def get_for_run(self, db_session: Session, run_id: int) -> [Range]:
        return db_session.query(self.model).filter(self.model.run_id == run_id).all()


range = CRUDRange(Range)
