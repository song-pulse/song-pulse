from collections import deque
from app import crud


class DataCleaning(object):
    # TODO include HRV computation and TEMP validation

    def __init__(self):

        self.settings = crud.setting.get(db, id=1)
        self.prev_eda_tend = deque([], maxlen=self.settings.duration)
        self.temp_data = deque([], maxlen=self.settings.temp_latency)

    def compute_hrv(self, normalized_ibi):
        # TODO
        # Root Mean Square of Successive Differences or RMSSD
        # np.sqrt(np.mean(np.square(np.diff(normalized_ibi))))
        # brauche ich den gleichen Intervall wie EDA oder ist da ein anderer zeitlicher Verzug drin?
        pass

    def detect_movement(self, acc_values):
        if acc_values[2] > acc_values[1] > acc_values[0]:
            diff = acc_values[2] - acc_values[1] - acc_values[0]
            if diff >= self.settings.acc_threshold:
                return True
        else:
            return False

    def detect_eda_increase(self):
        diff = self.prev_eda_tend[-1] - self.prev_eda_tend[0]
        # detect and increase if values have been increasing constantly and the difference is above threshold
        if all(i < j for i, j in zip(self.prev_eda_tend, self.prev_eda_tend[1:])) and diff >= self.settings.eda_threshold:
            return True
        else:
            return False

    def run(self, data, eda_baseline, temp_baseline):  # TODO extend with TEMP (keep values in memory for n iterations and check with "future" TEMP data)

        eda_tend = data.edaValue - eda_baseline
        self.prev_eda_tend.append(eda_tend)

        # for the first values where it is not possible to compare with the previous eda values and check the previous
        # acc, it takes the relative values only
        if len(self.prev_eda_tend) >= self.settings.duration:
            if self.detect_eda_increase() and not self.detect_movement(data.acc_values) and eda_tend > self.settings.stress_threshold:
                return 2
            elif eda_tend < (self.settings.stress_threshold * -1):
                return 0
            else:
                return 1
        else:
            if eda_tend > self.settings.stress_threshold:
                return 2
            elif eda_tend < (self.settings.stress_threshold * -1):
                return 0
            else:
                return 1

