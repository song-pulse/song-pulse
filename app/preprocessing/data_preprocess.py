from collections import deque, Counter
from app import crud
from app.api import deps


class DataCleaning(object):

    def __init__(self):

        self.settings = crud.setting.get(next(deps.get_db()), id=1)
        self.prev_eda_tend = deque([], maxlen=self.settings.duration)
        self.temp_data = deque([], maxlen=self.settings.temp_latency)
        self.prev_eda_stress = deque([], maxlen=self.settings.duration)
        self.prev_ibi = deque([], maxlen=self.settings.duration)
        self.prev_mean_rr = deque([], maxlen=self.settings.duration)
        self.prev_mean_rr_stress = deque([], maxlen=self.settings.duration)
        self.prev_mean_prr20 = deque([], maxlen=self.settings.duration)
        self.prev_prr20_stress = deque([], maxlen=self.settings.duration)

    def compute_mean_rr(self, ibi_value, ibi_baseline):
        relative_ibi = ibi_value - ibi_baseline
        self.prev_ibi.append(relative_ibi)
        mean_rr = sum(self.prev_mean_rr)/float(len(self.prev_mean_rr))
        self.prev_mean_rr.append(mean_rr)
        return mean_rr

    def compute_prr20(self):
        prr20 = ((len([i for i in self.prev_ibi if i >= 20])) * 100) / float(len(self.prev_ibi) - 1)
        self.prev_mean_prr20.append(prr20)
        return prr20

    def detect_movement(self, acc_values):
        if acc_values[2] > acc_values[1] > acc_values[0]:
            diff = acc_values[2] - acc_values[1] - acc_values[0]
            if diff >= self.settings.acc_threshold:
                return True
        else:
            return False

    def detect_stress_level(self, value, threshold):
        if value > threshold:
            return 2
        elif value < (threshold * -1):
            return 0
        else:
            return 1

    def validate_stress_level(self, data, prev_values, prev_stress, change, stress_threshold):
        stress_level = 1
        if len(prev_values) >= self.settings.duration:
            if not self.detect_movement(data.acc_values):
                if change:
                    stress_level = self.detect_stress_level(prev_values[-1], stress_threshold)
                else:
                    stress_level = prev_stress[-1]
            else:
                if not self.detect_movement(data.acc_values):
                    if prev_values[-1] > stress_threshold:
                        stress_level = 2
                    elif prev_values[-1] < (stress_threshold * -1):
                        stress_level = 0
        return stress_level

    def detect_change(self, prev_values, threshold):
        diff = prev_values[-1] - prev_values[0]
        # detect and increase if values have been increasing constantly and the difference is above threshold
        if all(i < j for i, j in zip(prev_values, prev_values[1:])) and diff >= threshold:
            return True
        elif all(i > j for i, j in zip(prev_values, prev_values[1:])) and diff >= threshold:
            return True
        else:
            return False

    def majority_vote(self, mean_rr_stress, eda_stress, prr20_stress):
        l = Counter([mean_rr_stress, eda_stress, prr20_stress])
        majority = l.most_common(1)[0][0]

        return majority

    def run(self, data, eda_baseline, ibi_baseline):
        # EDA
        eda_tend = data.edaValue - eda_baseline
        self.prev_eda_tend.append(eda_tend)

        eda_change = self.detect_change(self.prev_eda_tend, self.settings.eda_threshold)
        eda_stress = self.validate_stress_level(data, self.prev_eda_tend, self.prev_eda_stress,
                                                eda_change, self.settings.stress_threshold)
        self.prev_eda_stress.append(eda_stress)

        # MeanRR
        self.compute_mean_rr(data.ibi_value, ibi_baseline)
        mean_rr_change = self.detect_change(self.prev_mean_rr, self.settings.ibi_threshold)
        mean_rr_stress = self.validate_stress_level(data, self.prev_mean_rr, self.prev_mean_rr_stress,
                                                    mean_rr_change, self.settings.stress_threshold)

        self.prev_mean_rr_stress.append(mean_rr_stress)

        # PRR20
        self.compute_prr20()
        prr20_change = self.detect_change(self.prev_mean_prr20, threshold=0.0)
        prr20_stress = self.validate_stress_level(data, self.prev_mean_prr20, self.prev_prr20_stress,
                                                  prr20_change, self.settings.prr_threshold)

        return self.majority_vote(mean_rr_stress, eda_stress, prr20_stress)
