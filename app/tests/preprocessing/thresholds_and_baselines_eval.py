from app.preprocessing.unused.data_preprocess import DataCleaning
from app.tests.preprocessing.dummy_data import Settings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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

    @staticmethod
    def get_baseline(path):
        baseline_data = pd.read_csv(path, skiprows=1).mean(axis=0)
        if path.endswith('IBI.csv'):
            return baseline_data[1]
        else:
            return baseline_data[0]

    def define_eda_thresholds(self, measure, baseline_path, data_calm, data_stressed):
        baseline = self.get_baseline(baseline_path)
        values_middle = pd.read_csv(baseline_path).iloc[::40, :]
        values_calm = pd.read_csv(data_calm, skiprows=1).iloc[::40, :]
        values_stressed = pd.read_csv(data_stressed, skiprows=1).iloc[::40, :]
        relative_values_calm = values_calm - baseline
        relative_values_stressed = values_stressed - baseline
        relative_values_middle = values_middle - baseline
        # mean_values_calm = relative_values_calm.values.mean()
        # max_values_calm = relative_values_calm.values.max()
        # min_values_calm = relative_values_calm.values.min()
        # mean_values_stressed = relative_values_stressed.values.mean()
        # max_values_stressed = relative_values_stressed.values.max()
        # min_values_stressed = relative_values_stressed.values.min()
        cutoff = min(len(relative_values_calm), len(relative_values_stressed), len(relative_values_middle))

        # reduce length of series to be able to plot them in same time
        cutoff_calm = relative_values_calm.tail(cutoff)
        cutoff_middle = relative_values_middle.tail(cutoff)
        cutoff_stressed = relative_values_stressed.tail(cutoff)

        values = {'stressed': cutoff_stressed.values[:, 0],
                  'relaxed': cutoff_calm.values[:, 0],
                  'normal': cutoff_middle.values[:, 0],
                  # 'upper threshold': [self.settings.eda_threshold] * len(cutoff_middle),
                  # 'lower threshold': [self.settings.eda_threshold * -1] * (len(cutoff_middle))
                  }

        plot_df = pd.DataFrame(values)
        fig, ax = plt.subplots()
        plot_df.plot(kind='line', ax=ax)
        fig.savefig(measure + '_threshold_plot_alina.png')

    def load_ibi_data(self, baseline_path, ibi_path_calm, ibi_path_stressed):
        values_middle = pd.read_csv(baseline_path)
        values_calm = pd.read_csv(ibi_path_calm)
        values_stressed = pd.read_csv(ibi_path_stressed)
        normal = self.get_10_secs_intervals(values_middle)
        calm = self.get_10_secs_intervals(values_calm)
        stressed = self.get_10_secs_intervals(values_stressed)

        return normal, calm, stressed

    def get_10_secs_intervals(self, ibi_df):
        ibi_data = []
        time_passed = 0
        intervals = 0
        for interval in ibi_df.iterrows():
            print('time passed:', time_passed)
            print('interval:', interval[1][0])
            if interval[1][0] - time_passed >= 10:
                intervals += 1
                print('interval found', intervals)
                ibi_data.append(interval[1][1])
                time_passed = interval[1][0]
        return ibi_data

    def define_meanrr_thresholds(self, baseline_path, ibi_path_calm, ibi_path_stressed):
        normal, calm, stressed = self.load_ibi_data(baseline_path, ibi_path_calm, ibi_path_stressed)
        baseline = self.get_baseline(baseline_path)
        normal_mean_rr = []
        stressed_mean_rr = []
        calm_mean_rr = []
        for ibi in normal:
            normal_mean_rr.append(self.data_clean.compute_mean_rr(ibi, baseline))
        for ibi in stressed:
            stressed_mean_rr.append(self.data_clean.compute_mean_rr(ibi, baseline))
        for ibi in calm:
            calm_mean_rr.append(self.data_clean.compute_mean_rr(ibi, baseline))
        min_len = min(len(normal_mean_rr), len(stressed_mean_rr), len(calm_mean_rr))
        idx = len(normal_mean_rr) - min_len
        normal_mean_rr = normal_mean_rr[idx:]
        idx = len(stressed_mean_rr) - min_len
        stressed_mean_rr = stressed_mean_rr[idx:]
        idx = len(calm_mean_rr) - min_len
        calm_mean_rr = calm_mean_rr[idx:]
        fig, ax = plt.subplots()
        ax.plot(normal_mean_rr, label='Normal', color='green')
        ax.plot(stressed_mean_rr, label='Stressed', color='blue')
        ax.plot(calm_mean_rr, label='Calm', color='orange')
        plt.title('Mean RR comparison')
        legend = ax.legend(loc='center right', fontsize='x-large')
        fig.savefig('Mean_rr_comparison_plot_alina.png')
        fig.savefig(measure + '_threshold_plot_kathrin.png')

    def define_meanrr_thresholds(self):
        pass

    def define_prr20_thresholds(self):
        pass

    def visualize_avg_baseline(self, path):
        eda_values = pd.read_csv(path, skiprows=1).iloc[::40, :]
        baseline = 0.0
        counter = 0
        all_baselines = []
        for eda in eda_values.iterrows():
            current_value = eda[1][0]
            if baseline == 0.0:
                baseline = current_value
            else:
                baseline = float(np.divide((np.add(np.multiply(baseline, counter), current_value)), (counter + 1)))
            all_baselines.append(baseline)
        fig, ax = plt.subplots()
        ax.plot(all_baselines, label='avg baseline', color='blue')
        plt.title('EDA Baseline Long Time Average')
        fig.savefig('Baseline_plot_eda.png')


if __name__ == '__main__':
    evaluate = ThresholdsEval()
    measure = 'EDA'
    base_path = '../../../../../test_data/10.07.2020_Alina_Coding/' + measure + '.csv'
    data_path_stress = '../../../../../test_data/Alina_Stresstest_Silence/' + measure + '.csv'
    data_path_calm = '../../../../../test_data/20.07.2020_Alina_Relaxed/' + measure + '.csv'
    evaluate.define_meanrr_thresholds(base_path, data_path_calm, data_path_stress)
    evaluate.define_eda_thresholds(measure, baseline_path=base_path, data_calm=data_path_calm, data_stressed=data_path_stress)
    # random_path = '../../../../../test_data/random_recording/' + measure + '.csv'
    # evaluate.visualize_avg_baseline(random_path)


