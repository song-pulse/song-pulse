from collections import Counter

from sqlalchemy.orm import Session

from app import crud
from app.preprocessing.data_for_time import DataForTime
from app.preprocessing.min_max_detector import MinMaxDetector
from app.schemas.tendency import TendencyCreate
from app.spotify.song_queuer import is_queue_finished


def compute_prr20(ibi_values):
    if len(ibi_values) <= 1:
        return 0

    prev_value = None
    counter = 0
    for val in ibi_values:
        if prev_value:
            if (abs(val - prev_value)) * 1000 > 20:
                counter += 1
        prev_value = val

    return counter * 100 / float(len(ibi_values) - 1)


def compute_mean_rr(ibi_values):
    return sum(ibi_values) / float(len(ibi_values))


def majority_vote(db_session: Session, run_id: int, limit: int = 6):
    tendencies = crud.tendency.get_prev(db_session, run_id, limit)
    raw_tendencies = []
    for tendency in tendencies:
        raw_tendencies.append(tendency.eda)
        raw_tendencies.append(tendency.mean_rr)
        raw_tendencies.append(tendency.prr_20)
    l = Counter(raw_tendencies)
    return l.most_common(1)[0][0]


class StressChecker(object):

    def __init__(self, db_settings, db_session: Session):
        self.db_session = db_session
        self.detector = MinMaxDetector()
        self.settings = db_settings

    def run(self, data: DataForTime, part_id: int):
        if 0.0 in data.ibiValues:  # not enough values to determine anything, so we'll just assume balance.
            return None

        # MeanRR
        mean_rr = compute_mean_rr(data.ibiValues)

        # PRR20
        prr_20 = compute_prr20(data.ibiValues)

        eda_tendency, mean_rr_tendency, prr_20_tendency = self.detector.detect(db_session=self.db_session,
                                                                               eda_value=data.edaValue,
                                                                               mean_rr_value=mean_rr,
                                                                               prr_20_value=prr_20, run_id=data.runId)
        crud.tendency.create_with_run(db_session=self.db_session,
                                      obj_in=TendencyCreate(timestamp=data.timestamp,
                                                            eda=eda_tendency,
                                                            mean_rr=mean_rr_tendency,
                                                            prr_20=prr_20_tendency),
                                      run_id=data.runId)
        if is_queue_finished(db_session=self.db_session, run_id=data.runId):
            return majority_vote(self.db_session, data.runId)
