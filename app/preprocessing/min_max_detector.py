from sqlalchemy.orm import Session

from app import crud
from app.models.baseline import Baseline
from app.schemas.baseline import BaselineUpdate, BaselineCreate


def createBaselineUpdate(baseline: Baseline, new_min_max: float, min_changed: bool, max_changed: bool):
    if min_changed:
        new_min_max = (new_min_max + baseline.min_value) / 2
        return BaselineUpdate(participant_id=baseline.participant_id,
                              sensor_id=baseline.sensor_id,
                              min_value=new_min_max
                              )
    if max_changed:
        new_min_max = (new_min_max + baseline.max_value) / 2
        return BaselineUpdate(participant_id=baseline.participant_id,
                              sensor_id=baseline.sensor_id,
                              max_value=new_min_max
                              )


def checkMinMaxChange(min_value: float, max_value: float, current_value: float):
    if min_value < current_value:
        return False, True
    if max_value > current_value:
        return True, False
    return False, False


def checkMinMax(min_value: float, max_value: float, current_value: float):  # TODO is 25% good? should it be 10%?
    total_range = max_value - min_value
    current_position = current_value - min_value

    bottom_quarter = total_range / 4  # bottom 25%
    top_quarter = bottom_quarter * 3  # bottom 75%

    if current_position <= bottom_quarter:
        return 0
    if current_position >= top_quarter:
        return 2
    else:
        return 1


def createNewBaselines(db_session: Session, part_id: int):
    sensors = crud.sensor.get_multi(db_session=db_session)
    for sensor in sensors:
        crud.baseline.create(db_session=db_session,
                             obj_in=BaselineCreate(sensor_id=sensor.id, participant_id=part_id))


class MinMaxDetector:

    def detect(self, db_session: Session, eda_value: float, mean_rr_value: float, prr_20_value: float, part_id: int):
        eda_tendency = 1
        mean_rr_tendency = 1
        prr_20_tendency = 1
        baselines = crud.baseline.get_by_participant(db_session=db_session, participant_id=part_id)

        # if there are no baselines yet, create them!
        if len(baselines) == 0:
            createNewBaselines(db_session, part_id)
            baselines = crud.baseline.get_by_participant(db_session=db_session, participant_id=part_id)

        for baseline in baselines:
            if baseline.sensor.name == "EDA":  # EDA
                eda_tendency = checkMinMax(baseline.min_value, baseline.max_value, eda_value)
                max_changed, min_changed = checkMinMaxChange(baseline.min_value, baseline.max_value, eda_value)
                if max_changed or min_changed:
                    crud.baseline.update(db_session=db_session,
                                         db_obj=baseline,
                                         obj_in=createBaselineUpdate(baseline, eda_value, max_changed, min_changed))
            elif baseline.sensor.name == "IBI":  # MEAN RR
                mean_rr_tendency = checkMinMax(baseline.min_value, baseline.max_value, mean_rr_value)
                max_changed, min_changed = checkMinMaxChange(baseline.min_value, baseline.max_value, mean_rr_value)
                if max_changed or min_changed:
                    crud.baseline.update(db_session=db_session,
                                         db_obj=baseline,
                                         obj_in=createBaselineUpdate(baseline, mean_rr_value, max_changed, min_changed))
            elif baseline.sensor.name == "ACC":  # PRR 20 # TODO don't abuse ACC for prr 20 values, perhaps decoulpe baselines from sensors?
                prr_20_tendency = checkMinMax(baseline.min_value, baseline.max_value, prr_20_value)
                max_changed, min_changed = checkMinMaxChange(baseline.min_value, baseline.max_value, prr_20_value)
                if max_changed or min_changed:
                    crud.baseline.update(db_session=db_session,
                                         db_obj=baseline,
                                         obj_in=createBaselineUpdate(baseline, prr_20_value, max_changed, min_changed))

        return eda_tendency, mean_rr_tendency, prr_20_tendency
