from unittest import TestCase

from app.preprocessing.stress_validation import process_acc, detect_movement
from app.preprocessing.unused.data_preprocess import DataCleaning
from app.tests.preprocessing.dummy_data import Settings, Data


class PreprocessingTest(TestCase):

    def setUp(self):
        self.settings = Settings()
        self.data_clean = DataCleaning(db_settings=self.settings)

    def test_detect_increase_change(self):
        self.assertEqual(True, self.data_clean.detect_change([2.9, 3.1, 4.0], 0.3))

    def test_detect_decrease_change(self):
        self.assertTrue(self.data_clean.detect_change([3.1, 3.0, 2.8], 0.2))

    def test_detect_no_change(self):
        self.assertFalse(self.data_clean.detect_change([3.1, 3.1, 3.0], 0.5))

    def test_majority_vote(self):
        self.assertEqual(1, self.data_clean.majority_vote(1, 1, 2))

    def test_stress_level1(self):
        self.assertEqual(1, self.data_clean.detect_stress_level(0.25, 0.5))

    def test_stress_level2(self):
        self.assertEqual(2, self.data_clean.detect_stress_level(0.567, 0.5))

    def test_stress_level0(self):
        self.assertEqual(0, self.data_clean.detect_stress_level(-0.67, 0.5))

    def test_compute_mean_rr_first_run(self):
        ibi_value = 1.25
        ibi_baseline = 1.0
        self.assertEqual(0.25, self.data_clean.compute_mean_rr(ibi_value, ibi_baseline))

    def test_compute_mean_rr_later_run(self):
        ibi_value = 1.5
        ibi_baseline = 0.5
        for i in [0.75, 0.5, 1.2]:
            self.data_clean.prev_ibi.append(i)
        self.assertEqual(0.9, self.data_clean.compute_mean_rr(ibi_value, ibi_baseline))

    def test_prr20_first_run(self):
        self.assertEqual(0, self.data_clean.compute_prr20())

    def test_prr20_later_run(self):
        for i in [0.075, 0.019, 0.0006]:
            self.data_clean.prev_ibi.append(i)
        self.assertEqual(50, self.data_clean.compute_prr20())

    def test_process_acc_first_run(self):
        acc_values = [{'x': 0, 'y': 0, 'z': 0},
                      {'x': 0, 'y': 0, 'z': 0},
                      {'x': 1, 'y': 7, 'z': 50}]
        cumulated_acc = process_acc(acc_values)
        self.assertEqual([0.0, 0.0, 1.666666666666667], cumulated_acc)

    def test_process_acc_constant_move(self):
        acc_values = [{'x': 1, 'y': 7, 'z': 50},
                      {'x': 1, 'y': 7, 'z': 50},
                      {'x': 1, 'y': 7, 'z': 50},
                      {'x': 1, 'y': 7, 'z': 50},
                      {'x': 1, 'y': 7, 'z': 50},
                      {'x': 1, 'y': 7, 'z': 50},
                      {'x': 1, 'y': 7, 'z': 50}
                      ]

        cumulated_acc = process_acc(acc_values)
        self.assertEqual([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], cumulated_acc)

    def test_preprocess_acc_move(self):
        acc_values = [{'x': 1, 'y': 7, 'z': 50},
                      {'x': 3, 'y': 4, 'z': 20},
                      {'x': -1, 'y': 2, 'z': 10},
                      {'x': 5, 'y': -3, 'z': 24},
                      {'x': 12, 'y': 12, 'z': 12},
                      {'x': 14, 'y': 5, 'z': 23},
                      {'x': -5, 'y': 3, 'z': 30}]
        cumulated_acc = process_acc(acc_values)
        print('cumulated acc')
        print(cumulated_acc)
        self.assertEqual([0.0, 1.5, 2.6833333333333336, 3.7650000000000006,
                          4.7685, 5.624983333333335, 6.476770714285716], cumulated_acc)

    def test_detect_movement_false(self):
        acc_values = [{'x': 1, 'y': 1, 'z': 1},
                      {'x': 1, 'y': 2, 'z': 1},
                      {'x': 0, 'y': 1, 'z': 2},
                      {'x': -1, 'y': 0, 'z': 1}
                      ]
        self.assertFalse(detect_movement(acc_values, self.settings.acc_threshold))

    def test_detect_movement_true(self):
        acc_values = [{'x': 1, 'y': 1, 'z': 10},
                      {'x': 1, 'y': 2, 'z': 10},
                      {'x': 0, 'y': 1, 'z': 20},
                      {'x': -1, 'y': 0, 'z': 10}
                      ]
        self.assertTrue(detect_movement(acc_values, self.settings.acc_threshold))

    def test_validate_stress_first_iteration(self):
        data = Data(movement=False)
        self.assertEqual(1, self.data_clean.validate_stress_level(data,
                                                                  self.data_clean.prev_eda_tend,
                                                                  self.data_clean.prev_eda_stress,
                                                                  stress_threshold=self.data_clean.settings.stress_threshold,
                                                                  change=True))

    def test_validate_high_stress(self):
        data = Data(movement=False)
        prev_eda_values = [6, 12, 24]
        for i in prev_eda_values:
            self.data_clean.prev_eda_tend.append(i)

        self.assertEqual(2, self.data_clean.validate_stress_level(data,
                                                                  self.data_clean.prev_eda_tend,
                                                                  self.data_clean.prev_eda_stress,
                                                                  stress_threshold=self.data_clean.settings.stress_threshold,
                                                                  change=True))

    def test_validate_low_stress(self):
        data = Data(movement=False)
        prev_eda_values = [0.2, -0.11, -0.8]
        for i in prev_eda_values:
            self.data_clean.prev_eda_tend.append(i)

        self.assertEqual(0, self.data_clean.validate_stress_level(data,
                                                                  self.data_clean.prev_eda_tend,
                                                                  self.data_clean.prev_eda_stress,
                                                                  stress_threshold=self.data_clean.settings.stress_threshold,
                                                                  change=True))
