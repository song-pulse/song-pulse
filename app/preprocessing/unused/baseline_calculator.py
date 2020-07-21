import numpy as np
from sqlalchemy.orm import Session

from app import crud
from app.models.baseline import Baseline
from app.preprocessing.data_for_time import DataForTime
from app.schemas.baseline import BaselineUpdate, BaselineCreate


def createBaselineUpdate(baseline: Baseline, new_baseline: float):
    return BaselineUpdate(participant_id=baseline.participant_id,
                          sensor_id=baseline.sensor_id,
                          baseline=new_baseline,
                          counter=baseline.counter + 1
                          )


def calculateBaseline(baseline: float, counter: int, current_value: float):
    if baseline == 0.0:
        return current_value
    else:
        return float(np.divide((np.add(np.multiply(baseline, counter), current_value)), (counter + 1)))


def createNewBaselines(db_session: Session, part_id: int):
    sensors = crud.sensor.get_multi(db_session=db_session)
    for sensor in sensors:
        crud.baseline.create(db_session=db_session,
                             obj_in=BaselineCreate(sensor_id=sensor.id, participant_id=part_id))


class BaselineCalculator:

    def calculate(self, db_session: Session, data: DataForTime, part_id: int):
        eda_baseline = 0.0
        ibi_baseline = 0.0
        temp_baseline = 0.0
        baselines = crud.baseline.get_by_participant(db_session=db_session, participant_id=part_id)

        # if there are no baselines yet, create them!
        if len(baselines) == 0:
            createNewBaselines(db_session, part_id)
            baselines = crud.baseline.get_by_participant(db_session=db_session, participant_id=part_id)

        for baseline in baselines:
            if baseline.sensor.name == "EDA":
                eda_baseline = calculateBaseline(baseline.baseline, baseline.counter, data.edaValue)
                crud.baseline.update(db_session=db_session,
                                     db_obj=baseline,
                                     obj_in=createBaselineUpdate(baseline, eda_baseline))
            elif baseline.sensor.name == "IBI":
                ibi_baseline = calculateBaseline(baseline.baseline, baseline.counter, data.ibiValues[-1])
                crud.baseline.update(db_session=db_session,
                                     db_obj=baseline,
                                     obj_in=createBaselineUpdate(baseline, ibi_baseline))
            elif baseline.sensor.name == "TEMP":  # UNUSED
                temp_baseline = calculateBaseline(baseline.baseline, baseline.counter, data.tempValue)
                crud.baseline.update(db_session=db_session,
                                     db_obj=baseline,
                                     obj_in=createBaselineUpdate(baseline, temp_baseline))

        return eda_baseline, ibi_baseline
