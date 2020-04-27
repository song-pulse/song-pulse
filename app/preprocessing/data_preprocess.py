import pandas as pd
import numpy as np
from datetime import datetime


class DataCleaning(object):

    def __init__(self, smoothing, eda_baseline, eda_threshold, acc_threshold, acc_latency, min_duration):
        """

        :param smoothing: int: smoothing factor in seconds
        :param eda_baseline: str: "mean", "median" or "minimum"
        :param eda_threshold: float: indicates by how much the relative eda value needs to change to be counted as event
        :param acc_threshold: float: indicates by how much the acc value needs to change to be counted as event
        :param acc_latency: int: number of units of the smoothing factor before the event in eda that should be checked
                                for potential movements
        :param min_duration: int: minimum number of smoothing factor units for a specific tendency to be registered as "event"
        """
        self.smoothing = smoothing
        self.eda_baseline = eda_baseline
        self.eda_threshold = eda_threshold
        self.acc_threshold = acc_threshold
        self.acc_latency = acc_latency
        self.min_duration = min_duration

    def load_data(self, path, datatype):
        original_data = pd.read_csv(path + datatype + '.csv')
        measure_frequency = int(original_data.iloc[0][0])
        timestamp = float(original_data.columns[0])
        dt_object = datetime.fromtimestamp(timestamp)
        print('first measure at', dt_object)
        original_data = original_data.iloc[1:]
        # check for null values
        null_check = int(original_data.isnull().sum()[0])
        print("There are %s missing values in this %s file" % (null_check, datatype))
        # getting the average measure per second.
        return original_data, measure_frequency, timestamp

    def normalize_eda(self, path):
        original_data, measure_frequency, timestamp = self.load_data(path, datatype='EDA')
        normalized_data = original_data.groupby(np.arange(len(original_data)) // measure_frequency).mean()
        # smooth data by factor
        smoothed_data = normalized_data.groupby(np.arange(len(normalized_data)) // self.smoothing).mean()
        return smoothed_data

    def normalize_acc(self, path):
        # TODO needs to be changed to work with stream
        original_data, measure_frequency, timestamp = self.load_data(path, datatype='ACC')
        normalized_data = []
        prevx = 0
        prevy = 0
        prevz = 0
        summed = 0
        # Normalizing the ACC data with the formula on the Empatica website
        i = 0
        for row in original_data.iterrows():
            buffx = row[1][0]
            buffy = row[1][1]
            buffz = row[1][2]
            summed += max(abs(buffx - prevx), abs(buffy - prevy), abs(buffz - prevz))
            prevx = buffx
            prevy = buffy
            prevz = buffz
            if i + 1 == measure_frequency:
                normalized_data.append((summed / (i + 1)) * 0.9 + (summed / measure_frequency) * 0.1)
                i = 0
                summed = 0
            else:
                i += 1

        normalized_data = pd.DataFrame(normalized_data, columns=[timestamp])
        # smooth data by factor
        smoothed_data = normalized_data.groupby(np.arange(len(normalized_data)) // self.smoothing).mean()
        return smoothed_data

    def compute_baseline(self, normalized_data):
        # TODO adapt to long-term baseline
        base = 0
        if self.eda_baseline == 'minimum':
            base = float(np.min(normalized_data))
        elif self.eda_baseline == 'mean':
            base = float(np.mean(normalized_data))
        elif self.eda_baseline == 'median':
            base = float(np.median(normalized_data))
        else:
            print('please specify the baseline as either minimum, mean or median')
            print('returning original data')

        relative_data = normalized_data - base

        return relative_data

    def get_eda_tendency(self, smoothed_eda_data, smoothed_acc_data):
        # TODO adapt to streaming scenario
        start_time = float(smoothed_eda_data.columns[0])
        differences = smoothed_eda_data.diff()
        event_len = 0
        changed_by = 0
        prev_tendency = []
        events = []
        idx = 0
        for difference in differences.iterrows():
            difference = difference[1].values[0]
            if event_len <= self.min_duration and abs(difference) >= self.eda_threshold:
                if difference < 0:
                    current_tendency = 'negative'
                else:
                    current_tendency = 'positive'
                prev_tendency.append(current_tendency)
                if len(set(prev_tendency)) == 1:
                    changed_by += difference
                    event_len += 1
            elif event_len == self.min_duration:
                event_time = start_time + idx * self.smoothing
                event_len = 0
                changed_by = 0
                prev_tendency = []
                if not self.validate_events(idx, smoothed_acc_data):
                    events.append((event_time, changed_by))
            else:
                changed_by = 0
                event_len = 0
                prev_tendency = []
            idx += 1
        print('%s events detected in EDA data' % len(events))
        return events

    def validate_events(self, idx, smooth_acc):
        # TODO validate if approach is correct
        print('validating eda event')
        movement = True
        idx_start = idx - self.acc_latency
        acc_event_frame = smooth_acc.iloc[idx_start:idx].values
        for i in range(1, self.acc_latency):
            diff = float(acc_event_frame[i]) - float(acc_event_frame[i-1])
            if self.acc_threshold >= diff and diff <= 0:
                movement = False
                return movement

        return movement


if __name__ == '__main__':
    path = '../../../E4Data_2020_04_06/23.03.2020_Dimitri/'
    clean_data = DataCleaning(smoothing=3,
                              eda_baseline='minimum',
                              eda_threshold=0.01,
                              acc_threshold=0.5,
                              acc_latency=3,
                              min_duration=3)
    eda = clean_data.normalize_eda(path)
    acc = clean_data.normalize_acc(path)
    relative_eda = clean_data.compute_baseline(eda)
    clean_data.get_eda_tendency(relative_eda, acc)


