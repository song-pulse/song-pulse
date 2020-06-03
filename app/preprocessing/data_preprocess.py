from collections import deque, Counter
from app import crud


class DataCleaning(object):
    # TODO include HRV computation and majority voting
    #
     def __init__(self):
         print('hello')
    #
    #     self.settings = crud.setting.get(db, id=1)
    #     self.prev_eda_tend = deque([], maxlen=self.settings.duration)
    #     self.temp_data = deque([], maxlen=self.settings.temp_latency)
    #     self.prev_mean_rr = deque([], maxlen=self.settings.duration)
    #     self.prev_eda_stress = deque([], maxlen=self.settings.duration)
    #     self.prev_mean_rr_stress = deque([], maxlen=self.settings.duration)
    #     self.prev_prr20_stress = deque([], maxlen=self.settings.duration)
    #
    # def compute_mean_rr(self, ibi_value, ibi_baseline):
    #     relative_ibi = ibi_value - ibi_baseline
    #     self.prev_mean_rr.append(relative_ibi)
    #     return relative_ibi
    #
    # def compute_prr20(self):
    #     # TODO
    #     pass
    #
    # def detect_movement(self, acc_values):
    #     if acc_values[2] > acc_values[1] > acc_values[0]:
    #         diff = acc_values[2] - acc_values[1] - acc_values[0]
    #         if diff >= self.settings.acc_threshold:
    #             return True
    #     else:
    #         return False
    #
    # def detect_stress_level(self, value, threshold):
    #     if value > threshold:
    #         return 2
    #     elif value < (threshold * -1):
    #         return 0
    #     else:
    #         return 1
    #
    # def detect_eda_change(self):
    #     diff = self.prev_eda_tend[-1] - self.prev_eda_tend[0]
    #     # detect and increase if values have been increasing constantly and the difference is above threshold
    #     if all(i < j for i, j in zip(self.prev_eda_tend, self.prev_eda_tend[1:])) and diff >= self.settings.eda_threshold:
    #         return True
    #     elif all(i > j for i, j in zip(self.prev_eda_tend, self.prev_eda_tend[1:])) and diff >= self.settings.eda_threshold:
    #         return True
    #     else:
    #         return False
    #
    # def detect_mean_rr_change(self):
    #     # TODO add threshold
    #     # diff = self.prev_mean_rr[-1] - self.prev_mean_rr[0]
    #     if all(i < j for i, j in zip(self.prev_mean_rr, self.prev_mean_rr[1:])):
    #         return True
    #     elif all(i > j for i, j in zip(self.prev_mean_rr, self.prev_mean_rr[1:])):
    #         return True
    #     else:
    #         return False
    #
    # def majority_vote(self, mean_rr_stress, eda_stress, prr20_stress):
    #     l = Counter([mean_rr_stress, eda_stress, prr20_stress])
    #     majority = l.most_common(1)[0][0]
    #
    #     return majority
    #
    # def run(self, data, eda_baseline, ibi_baseline):
    #     # return 1 value per loop
    #     eda_tend = data.edaValue - eda_baseline
    #     self.prev_eda_tend.append(eda_tend)
    #
    #     # for the first values where it is not possible to compare with the previous eda values and check the previous
    #     # acc, it takes the relative values only
    #     eda_stress = 1
    #     if len(self.prev_eda_tend) >= self.settings.duration:
    #         if not self.detect_movement(data.acc_values):
    #             if self.detect_eda_change():
    #                 eda_stress = self.detect_stress_level(eda_tend, self.settings.stress_threshold)
    #             else:
    #                 eda_stress = self.prev_eda_stress[-1]
    #     else:
    #         if not self.detect_movement(data.acc_values):
    #             if eda_tend > self.settings.stress_threshold:
    #                 eda_stress = 2
    #             elif eda_tend < (self.settings.stress_threshold * -1):
    #                 eda_stress = 0
    #     self.prev_eda_stress.append(eda_stress)
    #
    #     # MeanRR
    #     mean_rr = self.compute_mean_rr(data.ibi_value, ibi_baseline)
    #     mean_rr_stress = 1
    #     if len(self.prev_mean_rr) >= self.settings.duration:
    #         if not self.detect_movement(data.acc_values):
    #             if self.detect_mean_rr_change():
    #                 # TODO change with mean rr threshold
    #                 mean_rr_stress = self.detect_stress_level(mean_rr, self.settings.stress_threshold)
    #             else:
    #                 mean_rr_stress = self.prev_mean_rr_stress[-1]
    #     else:
    #         if not self.detect_movement(data.acc_values):
    #             # TODO exchange threshold
    #             if mean_rr > self.settings.stress_threshold:
    #                 mean_rr_stress = 2
    #             elif mean_rr < (self.settings.stress_threshold * -1):
    #                 mean_rr_stress = 0
    #     self.prev_mean_rr_stress.append(mean_rr_stress)
    #
    #     # TODO compute prr20Stress
    #     prr20_stress = 1
    #
    #     return self.majority_vote(mean_rr_stress, eda_stress, prr20_stress)
    #
