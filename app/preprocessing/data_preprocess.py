import itertools
from collections import deque, Counter
import numpy as np


class DataCleaning(object):

    def __init__(self, db_settings):

        self.settings = db_settings
        self.prev_eda_tend = deque([], maxlen=self.settings.duration)
        self.temp_data = deque([], maxlen=self.settings.temp_latency)
        self.prev_eda_stress = deque([1], maxlen=self.settings.duration)
        self.prev_ibi = deque([], maxlen=self.settings.duration)
        self.prev_mean_rr = deque([], maxlen=self.settings.duration)
        self.prev_mean_rr_stress = deque([1], maxlen=self.settings.duration)
        self.prev_mean_prr20 = deque([], maxlen=self.settings.duration)
        self.prev_prr20_stress = deque([1], maxlen=self.settings.duration)
        self.prev_raw_acc = {'x': 0, 'y': 0, 'z': 0}
        self.prev_cumulated_acc = deque([0.0], maxlen=self.settings.duration)
        # 6 is based on getting data every 10 secs so the list represents the accs of one number of measures per minute
        self.summarized_accs = deque([0], maxlen=6)

    def compute_mean_rr(self, ibi_value, ibi_baseline):
        relative_ibi = ibi_value - ibi_baseline
        self.prev_ibi.append(relative_ibi)
        mean_rr = sum(self.prev_ibi)/float(len(self.prev_ibi))
        self.prev_mean_rr.append(mean_rr)
        return mean_rr

    def compute_prr20(self):
        if len(self.prev_ibi) <= 1:
            return 0
        prr20 = ((len([i for i in self.prev_ibi if (i * 1000) >= 20])) * 100) / float(len(self.prev_ibi)-1)
        self.prev_mean_prr20.append(prr20)
        return prr20

    def detect_movement(self, acc_values):
        self.process_acc(acc_values)
        if np.mean(self.prev_cumulated_acc) >= self.settings.acc_threshold:
            return True
        else:
            return False

    def process_acc(self, acc_values):
        for value in acc_values:
            summarized_acc = max(abs(value['x'] - self.prev_raw_acc['x']), abs(value['y'] - self.prev_raw_acc['y']),
                                 abs(value['z'] - self.prev_raw_acc['z']))
            self.summarized_accs.append(summarized_acc)
            filtered_acc = self.prev_cumulated_acc[-1] * 0.9 + (sum(self.summarized_accs) /
                                                                float(len(self.summarized_accs)) * 0.1)
            self.prev_cumulated_acc.append(filtered_acc)
            self.prev_raw_acc['x'] = value['x']
            self.prev_raw_acc['y'] = value['y']
            self.prev_raw_acc['z'] = value['z']

            return filtered_acc

    @staticmethod
    def detect_stress_level(value, threshold):
        if value > threshold:
            return 2
        elif value < (threshold * -1):
            return 0
        else:
            return 1

    def validate_stress_level(self, data, prev_values, prev_stress, change, stress_threshold):
        stress_level = 1
        if len(prev_stress) == 0:
            return 1
        if len(prev_values) >= self.settings.duration:
            if not self.detect_movement(data.accValues):
                if change:
                    stress_level = self.detect_stress_level(prev_values[-1], stress_threshold)
                else:
                    stress_level = prev_stress[-1]
            else:
                if not self.detect_movement(data.accValues):
                    if prev_values[-1] > stress_threshold:
                        stress_level = 2
                    elif prev_values[-1] < (stress_threshold * -1):
                        stress_level = 0
        return stress_level

    @staticmethod
    def detect_change(prev_values, threshold):
        if len(prev_values) == 0:
            return False
        diff = abs(prev_values[-1] - prev_values[0])
        sliced_prev_values = deque(itertools.islice(prev_values, 1, len(prev_values)))
        # detect and increase if values have been increasing constantly and the difference is above threshold
        if all(i < j for i, j in zip(prev_values, sliced_prev_values)) and diff >= threshold:
            return True
        elif all(i > j for i, j in zip(prev_values, sliced_prev_values)) and diff >= threshold:
            return True
        else:
            return False

    @staticmethod
    def majority_vote(mean_rr_stress, eda_stress, prr20_stress):
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
        self.compute_mean_rr(data.ibiValue, ibi_baseline)
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
