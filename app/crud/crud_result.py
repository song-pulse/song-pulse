from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.result import Result
from app.schemas.result import ResultCreate, ResultUpdate


class CRUDResult(CRUDBase[Result, ResultCreate, ResultUpdate]):

    def create_with_run(self, db_session: Session, obj_in: ResultCreate,
                        run_id: int) -> Result:
        obj_in_data = jsonable_encoder(obj_in)
        fresh_result = self.model(**obj_in_data, run_id=run_id)
        db_session.add(fresh_result)
        db_session.commit()
        db_session.refresh(fresh_result)
        return fresh_result

    def get_prev(self, db_session: Session, run_id: int, limit: int = 3) -> [Result]:
        return db_session.query(self.model).filter(self.model.run_id == run_id) \
            .order_by(self.model.id.desc()).limit(limit).all()

    def get_last_queued(self, db_session: Session, run_id: int) -> Result:
        return db_session.query(self.model).filter(self.model.run_id == run_id) \
            .filter(self.model.song_queued)\
            .order_by(self.model.id.desc()).first()


result = CRUDResult(Result)
