from unittest import TestCase
from app.tests.preprocessing.dummy_data import Settings
from app.preprocessing.data_preprocess import DataCleaning


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


