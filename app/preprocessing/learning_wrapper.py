from app import crud
from app.api import deps
from app.preprocessing.data_for_time import DataForTime
from app.preprocessing.data_preprocess_perecentile import DataCleaning


class LearningWrapper:

    def __init__(self):
        self.dbSession = next(deps.get_db())
        self.cleaning = DataCleaning(db_settings=crud.setting.get(self.dbSession), db_session=self.dbSession)

    def run(self, data: DataForTime, part_id: int):
        return self.cleaning.run(data=data, part_id=part_id)

    def get_db_session(self):
        return self.dbSession
