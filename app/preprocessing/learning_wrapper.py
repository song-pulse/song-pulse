from app.mltraining.q_learning_music import SongPulseAgent
from app.preprocessing.data_preprocess import DataCleaning


class LearningWrapper:

    def __init__(self):
        self.edaCount = 0
        self.edaBaseline = 0
        self.tempCount = 0
        self.tempBaseline = 0
        self.learning = SongPulseAgent()
        self.cleaning = DataCleaning(smoothing=3,
                                     eda_baseline='mean',
                                     eda_threshold=0.01,
                                     acc_threshold=0.5,
                                     acc_latency=3,
                                     temp_baseline=0.3,
                                     temp_latency=3,
                                     min_duration=3,
                                     upper_stress_threshold=0.1,
                                     lower_stress_threshold=-0.1)  # TODO remove / get them from the database

    def calculate_eda_baseline(self, current_value):  # TODO get baseline from database
        if self.edaBaseline == 0:
            self.edaBaseline = current_value
        else:
            self.edaBaseline = ((self.edaBaseline * self.edaCount) + current_value) / (self.edaCount + 1)
        self.edaCount = self.edaCount + 1

    def calculate_temp_baseline(self, current_value):
        if self.tempBaseline == 0:
            self.tempBaseline = current_value
        else:
            self.tempBaseline = ((self.tempBaseline * self.edaCount) + current_value) / (self.edaCount + 1)
        self.edaCount = self.edaCount + 1

    def run(self, data):
        self.calculate_eda_baseline(data.edaValue)
        self.calculate_temp_baseline(data.edaValue)

        tendency = self.cleaning.run(data, self.edaBaseline, self.tempBaseline)
        return self.learning.run_with_tendency(tendency)
