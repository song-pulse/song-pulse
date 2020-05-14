from app.mltraining.q_learning_music import SongPulseAgent
from app.preprocessing.data_preprocess import DataCleaning


class LearningWrapper:

    def __init__(self):
        self.edaCount = 0
        self.edaBaseline = 0
        self.tempCount = 0
        self.tempBaseline = 0
        self.learning = SongPulseAgent()
        self.cleaning = DataCleaning()

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
        print(tendency)
        return self.learning.run_with_tendency(tendency)
