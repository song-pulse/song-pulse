from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.tendency import Tendency
from app.schemas.tendency import TendencyCreate, TendencyUpdate


class CRUDTendency(CRUDBase[Tendency, TendencyCreate, TendencyUpdate]):

    def create_with_run(self, db_session: Session, obj_in: TendencyCreate,
                        run_id: int) -> Tendency:
        obj_in_data = jsonable_encoder(obj_in)
        fresh_result = self.model(**obj_in_data, run_id=run_id)
        db_session.add(fresh_result)
        db_session.commit()
        db_session.refresh(fresh_result)
        return fresh_result

    def get_prev(self, db_session: Session, run_id: int, limit: int = 6) -> [Tendency]:
        return db_session.query(self.model).filter(self.model.run_id == run_id) \
            .order_by(self.model.timestamp.desc()).limit(limit).all()


tendency = CRUDTendency(Tendency)
