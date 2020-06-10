from app import crud
from app.api import deps
from app.preprocessing.data_for_time import DataForTime
from app.preprocessing.learning_wrapper import LearningWrapper
from app.schemas.result import ResultCreate


class ProcessValue:

    @staticmethod
    def single_value(part_id, rec_id, run_id, values):
        data = ProcessValue.convert_to_data_for_time(values, run_id)
        learning = LearningWrapper()
        song_id = learning.run(data, part_id)
        result = ResultCreate(timestamp=data.timestamp, song_id=song_id, verdict=-1,
                              input=str(data))
        crud.result.create_with_run(db_session=next(deps.get_db()), obj_in=result, run_id=run_id)

    @staticmethod
    def convert_to_data_for_time(values, run_id):
        data = DataForTime()
        data.timestamp = values.timestamp
        data.runId = run_id
        data.edaValue = values.eda
        data.ibiValue = values.ibi
        data.tempValue = values.temp
        data.accValues = [values.acc_x, values.acc_y, values.acc_z]
        return data
