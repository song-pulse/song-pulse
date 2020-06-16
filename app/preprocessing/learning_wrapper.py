import numpy as np
from app import crud
from app.api import deps
from app.mltraining.q_learning_music import SongPulseAgent
from app.preprocessing.data_for_time import DataForTime
from app.preprocessing.data_preprocess import DataCleaning
from app.models.baseline import Baseline
from app.schemas.baseline import BaselineUpdate, BaselineCreate


class LearningWrapper:

    def __init__(self):
        self.dbSession = next(deps.get_db())
        self.learning = SongPulseAgent()
        self.cleaning = DataCleaning(crud.setting.get(self.dbSession, id=1))

    @staticmethod
    def calculate_baseline(baseline: float, counter: int, current_value: float):
        if baseline == 0.0:
            return current_value
        else:
            return float(np.divide((np.add(np.multiply(baseline, counter), current_value)), (counter + 1)))

    @staticmethod
    def createBaselineUpdate(baseline: Baseline, new_baseline: float):
        return BaselineUpdate(participant_id=baseline.participant_id,
                              sensor_id=baseline.sensor_id,
                              baseline=new_baseline,
                              counter=baseline.counter+1
                              )

    def createNewBaselines(self, part_id: int):
        sensors = crud.sensor.get_multi(db_session=self.dbSession)
        for sensor in sensors:
            crud.baseline.create(db_session=self.dbSession, obj_in=BaselineCreate(sensor_id=sensor.id, participant_id=part_id))

    def run(self, data: DataForTime, part_id: int):
        eda_baseline = 0.0
        ibi_baseline = 0.0
        baselines = crud.baseline.get_by_participant(db_session=self.dbSession, participant_id=part_id)

        # if there are no baselines yet, create them!
        if len(baselines) == 0:
            self.createNewBaselines(part_id)
            baselines = crud.baseline.get_by_participant(db_session=self.dbSession, participant_id=part_id)

        for baseline in baselines:
            if baseline.sensor.name == "EDA":
                eda_baseline = self.calculate_baseline(baseline.baseline, baseline.counter, data.edaValue)
                crud.baseline.update(db_session=self.dbSession,
                                     db_obj=baseline,
                                     obj_in=self.createBaselineUpdate(baseline, eda_baseline))
            elif baseline.sensor.name == "IBI":
                ibi_baseline = self.calculate_baseline(baseline.baseline, baseline.counter, data.ibiValue)
                crud.baseline.update(db_session=self.dbSession,
                                     db_obj=baseline,
                                     obj_in=self.createBaselineUpdate(baseline, ibi_baseline))
            elif baseline.sensor.name == "TEMP":
                temp_baseline = self.calculate_baseline(baseline.baseline, baseline.counter, data.tempValue)
                crud.baseline.update(db_session=self.dbSession,
                                     db_obj=baseline,
                                     obj_in=self.createBaselineUpdate(baseline, temp_baseline))

        tendency = self.cleaning.run(data, eda_baseline, ibi_baseline)
        return self.learning.run_with_tendency(tendency, data.timestamp, data.runId, part_id)
