from typing import List

from sqlalchemy.orm import Session

from app import crud
from app.models.value import Value
from app.preprocessing.data_for_time import DataForTime
from app.preprocessing.learning_wrapper import LearningWrapper
from app.schemas.result import ResultCreate
from app.schemas.timestamp_values import TimestampValues


class ProcessValue:

    @staticmethod
    def single_value(part_id: int, rec_id: int, run_id: int, values: TimestampValues):
        learning = LearningWrapper()
        db_session = learning.get_db_session()

        data = ProcessValue.convert_to_data_for_time(db_session, values, rec_id, run_id)
        song_id = learning.run(data, part_id)

        result = ResultCreate(timestamp=data.timestamp, song_id=song_id, verdict=-1, input=str(data))
        crud.result.create_with_run(db_session=db_session, obj_in=result, run_id=run_id)

    @staticmethod
    def convert_to_data_for_time(db_session: Session, values: TimestampValues, rec_id: int, run_id: int) -> DataForTime:
        data = DataForTime()
        data.timestamp = values.timestamp
        data.runId = run_id
        data.edaValue = values.eda
        data.ibiValue = values.ibi
        data.tempValue = values.temp
        historic_acc = ProcessValue.get_historic_acc(db_session, values.timestamp, rec_id)

        if len(historic_acc) > 0:
            data.accValues[1] = {"x": historic_acc[0].value1, "y": historic_acc[0].value2, "z": historic_acc[0].value3}
        if len(historic_acc) > 1:
            data.accValues[0] = {"x": historic_acc[1].value1, "y": historic_acc[1].value2, "z": historic_acc[1].value3}
        data.accValues[2] = {"x": values.acc_x, "y": values.acc_y, "z": values.acc_z}
        return data

    @staticmethod
    def get_historic_acc(db_session: Session, timestamp: int, rec_id: int) -> List[Value]:
        file_id = crud.file.get_id_for_recording_and_name(db_session, rec_id, "ACC")
        return crud.value.get_prev_two(db_session, file_id, timestamp)
