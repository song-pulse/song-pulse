from app.preprocessing.data_preprocess import DataCleaning
from app.tests.preprocessing.dummy_data import Settings
import pandas as pd
import numpy as np


class ThresholdsEval:

    def __init__(self):
        self.settings = Settings()
        self.data_clean = DataCleaning(db_settings=self.settings)

    def prepare_simulation_data(self, path):
        all_data = pd.read_csv(path, skiprows=1)
        # TODO get every 8th 9th and 10th second
        x_0 = 0
        x_1 = -1
        x_2 = -2
        acc_data = []
        while x_0 < len(all_data):
            acc_triple = []
            acc_row = all_data.iloc[x_0]
            acc_dict = {'x': acc_row.iloc[0], 'y': acc_row.iloc[1], 'z': acc_row.iloc[2]}
            acc_triple.append(acc_dict)
            if x_1 > 0:
                acc_row = all_data.iloc[x_1]
                acc_dict = {'x': acc_row.iloc[0], 'y': acc_row.iloc[1], 'z': acc_row.iloc[2]}
                acc_triple.append(acc_dict)

                acc_row = all_data.iloc[x_2]
                acc_dict = {'x': acc_row.iloc[0], 'y': acc_row.iloc[1], 'z': acc_row.iloc[2]}
                acc_triple.append(acc_dict)
            else:
                acc_dict = {'x': 0, 'y': 0, 'z': 0}
                acc_triple.insert(0, acc_dict)
                acc_dict = {'x': 0, 'y': 0, 'z': 0}
                acc_triple.insert(0, acc_dict)
            acc_data.append(acc_triple)
            x_0 += 320
            x_1 += 320
            x_2 += 320

        return acc_data

    def test_acc_preprocessing(self, path):
        acc_simulation = evaluate.prepare_simulation_data(path)
        all_cumulated_values = []
        for acc_triplet in acc_simulation:
            all_cumulated_values.append(self.data_clean.process_acc(acc_triplet))
        print('maximum acc value', max(all_cumulated_values))
        print('average acc value', np.mean(all_cumulated_values))

    def test_detect_movement(self, path):
        acc_simulation = evaluate.prepare_simulation_data(path)
        movement_detected = 0
        for acc_triplet in acc_simulation:
            if self.data_clean.detect_movement(acc_triplet):
                movement_detected += 1
        print(movement_detected)
        print(len(acc_simulation))


if __name__ == '__main__':
    evaluate = ThresholdsEval()
    evaluate.test_detect_movement('../../../../../test_data/Kathrin_stresstest_2020-07-10/ACC.csv')


