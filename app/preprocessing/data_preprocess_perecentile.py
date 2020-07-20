from collections import Counter

from sqlalchemy.orm import Session

from app.preprocessing.data_for_time import DataForTime
from app.preprocessing.min_max_detector import MinMaxDetector


def compute_prr20(ibi_values):
    if len(ibi_values) <= 1:
        return 0
    return ((len([i for i in ibi_values if (i * 1000) >= 20])) * 100) / float(len(ibi_values) - 1)


def compute_mean_rr(ibi_values):
    return sum(ibi_values) / float(len(ibi_values))


class DataCleaning(object):

    def __init__(self, db_settings, db_session: Session):
        self.db_session = db_session
        self.detector = MinMaxDetector()
        self.settings = db_settings

    @staticmethod
    def majority_vote(mean_rr_stress, eda_stress, prr20_stress):
        l = Counter([mean_rr_stress, eda_stress, prr20_stress])
        majority = l.most_common(1)[0][0]
        return majority

    def run(self, data: DataForTime, part_id: int):
        if 0.0 in data.ibiValues:  # not enough values to determine anything, so we'll just assume balance.
            return 1

        # MeanRR
        mean_rr = compute_mean_rr(data.ibiValues)
        # TODO validate mean_rr with ACC

        # PRR20
        prr_20 = compute_prr20(data.ibiValues)
        # TODO validate prr20 with ACC

        eda_tendency, mean_rr_tendency, prr_20_tendency = self.detector.detect(db_session=self.db_session,
                                                                               eda_value=data.edaValue,
                                                                               mean_rr_value=mean_rr,
                                                                               prr_20_value=prr_20, part_id=part_id)
        return self.majority_vote(eda_tendency, mean_rr_tendency, prr_20_tendency)
