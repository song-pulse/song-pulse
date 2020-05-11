import pandas as pd
import numpy as np
from datetime import datetime


class DataCleaning(object):
    # TODO include HRV computation
    # Heart rate variability increases during relaxing and recovering activities and decreases during stress.
    # "The most popular HRV metric is the Root Mean Square of Successive Differences or RMSSD"
    # np.sqrt(np.mean(np.square(np.diff(rr))))

    def __init__(self, smoothing,
                 eda_baseline, eda_threshold,
                 acc_threshold, acc_latency,
                 temp_baseline, temp_latency,
                 min_duration, upper_stress_threshold,
                 lower_stress_threshold):
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
        self.upper_threshold = upper_stress_threshold
        self.lower_threshold = lower_stress_threshold
        self.eda_baseline = eda_baseline
        self.eda_threshold = eda_threshold
        self.acc_threshold = acc_threshold
        self.acc_latency = acc_latency
        self.temp_baseline = temp_baseline
        self.temp_latency = temp_latency
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

    def load_ibi(self, path):
        # TODO remove and adapt to streaming
        original_data = pd.read_csv(path + "IBI.csv")
        timestamp = float(original_data.columns[0])
        dt_object = datetime.fromtimestamp(timestamp)
        print('first measure at', dt_object)
        original_data = original_data.iloc[1:]
        # check for null values
        null_check = int(original_data.isnull().sum()[0])
        print("There are %s missing values in this IBI file" % null_check)

        return original_data, timestamp

    def normalize_eda_and_temp(self, path, datatype):
        original_data, measure_frequency, timestamp = self.load_data(path, datatype=datatype)
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

    def normalize_ibi(self, path):
        # TODO match timestamp with EDA timestamp and get same time interval
        ibi, ibi_start = clean_data.load_ibi(path)


        pass

    def compute_hrv(self, normalized_ibi):
        # TODO
        # Root Mean Square of Successive Differences or RMSSD
        # np.sqrt(np.mean(np.square(np.diff(normalized_ibi))))
        # brauche ich den gleichen Intervall wie EDA oder ist da ein anderer zeitlicher Verzug drin?
        pass

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

    def get_eda_tendency(self, smoothed_eda_data, smoothed_acc_data, smoothed_temp_data):
        # TODO adapt to streaming scenario
        start_time = float(smoothed_eda_data.columns[0])
        differences = smoothed_eda_data.diff()
        event_len = 0
        # changed_by = 0
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
                    # changed_by += difference
                    event_len += 1
            elif event_len == self.min_duration:
                event_time = start_time + idx * self.smoothing
                event_len = 0
                # changed_by = 0
                prev_tendency = []
                eda_value = smoothed_eda_data.iloc[idx].values[0]
                if self.validate_events(idx, smoothed_acc_data, smoothed_temp_data) and eda_value >= self.upper_threshold:
                    stress_level = 1
                elif eda_value <= self.lower_threshold:
                    stress_level = -1
                else:
                    stress_level = 0

                events.append((event_time, stress_level))
            else:
                # changed_by = 0
                event_len = 0
                prev_tendency = []
            idx += 1
        high_stess_events = len([e for e in events if e[1] > 0])
        low_stess_events = len([e for e in events if e[1] < 0])
        print('===')
        print('Overall %s events detected in EDA data' % len(events))
        print('%s high stress events' % high_stess_events)
        print('%s low stress events' % low_stess_events)
        print('===')
        print('\n\n')

        return events

    def validate_events(self, idx, smooth_acc, smooth_temp):
        # TODO validate if approach is correct
        # TODO extract event detection function for ACC and TEMP
        # Movement when relative ACC value increases over n time intervals (n=acc_latency)
        stress = False
        print('validating eda event')
        movement = False
        # determining the relevant data according to latency variable
        idx_start = idx - self.acc_latency
        acc_event_frame = smooth_acc.iloc[idx_start:idx].values
        movement_factor = 0
        for i in range(1, self.acc_latency):
            diff = float(acc_event_frame[i]) - float(acc_event_frame[i-1])
            if self.acc_threshold <= diff and diff > 0:
                print("ACC value is increasing")
                movement_factor += 1
        # If movement consistently increased since start of latency factor, eda event was caused by movement
        print("movement factor", movement_factor)
        if movement_factor == self.acc_latency:
            print("setting movement to True")
            movement = True
        # TEMP: Stress when relative skin temperature decreases over n time intervals
        # print("start checking TEMP data")
        # temp_decrease = False
        # temp_end = idx + self.temp_latency + 1
        # temp_event_frame = smooth_temp.iloc[idx:temp_end].values
        # temp_factor = 0
        # for i in range(0, self.temp_latency):
        #     temp_diff = float(temp_event_frame[i]) - float(temp_event_frame[i+1])
        #     if temp_diff < 0:
        #         temp_factor += 1
        # print("temperature factor", temp_factor)
        # if temp_factor == self.temp_latency:
        #     print("setting temp_decrease to True")
        #     temp_decrease = True

        if not movement:  # and temp_decrease:
            stress = True

        return stress


if __name__ == '__main__':
    path = '../../../E4Data_2020_04_06/01.04.2020_Kathrin/'
    clean_data = DataCleaning(smoothing=3,
                              eda_baseline='mean',
                              eda_threshold=0.01,
                              acc_threshold=0.5,
                              acc_latency=3,
                              temp_baseline=0.3,
                              temp_latency=3,
                              min_duration=3,
                              upper_stress_threshold=0.1,
                              lower_stress_threshold=-0.1)
    # clean_data.normalize_ibi(path)
    eda = clean_data.normalize_eda_and_temp(path, datatype="EDA")
    acc = clean_data.normalize_acc(path)
    temp = clean_data.normalize_eda_and_temp(path, datatype="TEMP")
    relative_eda = clean_data.compute_baseline(eda)
    relative_temp = clean_data.compute_baseline(temp)
    clean_data.get_eda_tendency(relative_eda, acc, relative_temp)


