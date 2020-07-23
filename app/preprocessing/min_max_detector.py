from sqlalchemy.orm import Session

from app import crud
from app.models.range import Range
from app.schemas.range import RangeUpdate, RangeCreate


def createRangeUpdate(range: Range, new_min_max: float, min_changed: bool, max_changed: bool):
    if min_changed:
        new_min_max = (new_min_max + (range.min * range.counter)) / (range.counter + 1)
        # the longer the session the less change we want to see in the min max values
        return RangeUpdate(name=range.name,
                           counter=range.counter + 1,
                           min_value=new_min_max
                           )
    if max_changed:
        new_min_max = (new_min_max + (range.max * range.counter)) / (range.counter + 1)
        return RangeUpdate(name=range.name,
                           counter=range.counter + 1,
                           max_value=new_min_max
                           )


def checkMinMaxChange(min_value: float, max_value: float, current_value: float):
    if min_value < current_value:
        return False, True
    if max_value > current_value:
        return True, False
    return False, False


def checkMinMaxEDA(min_value: float, max_value: float, current_value: float):
    total_range = max_value - min_value
    percentile10 = total_range / 10  # 10% from bottom
    percentile2 = total_range / 50  # 2% from top
    top = max_value - percentile2
    bottom = min_value + percentile10

    if current_value <= bottom:
        return 0
    if current_value >= top:
        return 2
    else:
        return 1


def checkMinMaxRR(min_value: float, max_value: float, current_value: float):
    total_range = max_value - min_value
    percentile10 = total_range / 10  # 10% from top
    top = max_value - percentile10
    bottom = min_value + percentile10

    if current_value <= bottom:
        return 2
    if current_value >= top:
        return 0
    else:
        return 1


def createNewRanges(db_session: Session, range_names: [str], run_id: int):
    for name in range_names:
        crud.range.create_with_run(db_session=db_session,
                                   obj_in=RangeCreate(name=name), run_id=run_id)


def update_range_if_needed(range: Range, db_session: Session, current_value: float):
    max_changed, min_changed = checkMinMaxChange(range.min, range.max, current_value)
    if max_changed or min_changed:
        crud.range.update(db_session=db_session,
                          db_obj=range,
                          obj_in=createRangeUpdate(range, current_value, max_changed, min_changed))


class MinMaxDetector:

    def detect(self, db_session: Session, eda_value: float, mean_rr_value: float, prr_20_value: float, run_id: int):
        range_names = ["eda", "meanrr", "prr20"]
        eda_tendency = 1
        mean_rr_tendency = 1
        prr_20_tendency = 1
        ranges = crud.range.get_for_run(db_session=db_session, run_id=run_id)

        # if there are no baselines yet, create them!
        if len(ranges) == 0:
            createNewRanges(db_session, range_names, run_id)
            ranges = crud.range.get_for_run(db_session=db_session, run_id=run_id)

        for range in ranges:
            if range.name == range_names[0]:
                eda_tendency = checkMinMaxEDA(range.min, range.max, eda_value)
                update_range_if_needed(range, db_session, eda_value)
            if range.name == range_names[1]:
                mean_rr_tendency = checkMinMaxRR(range.min, range.max, mean_rr_value)
                update_range_if_needed(range, db_session, mean_rr_value)
            elif range.name == range_names[2]:
                prr_20_tendency = checkMinMaxRR(range.min, range.max, prr_20_value)
                update_range_if_needed(range, db_session, prr_20_value)

        return eda_tendency, mean_rr_tendency, prr_20_tendency
