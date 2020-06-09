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


result = CRUDResult(Result)
