from unittest import TestCase
from app.preprocessing.data_preprocess import DataCleaning


class PreprocessingTest(TestCase):

    def test_detect_increase_change(self):
        self.assertEqual(True, DataCleaning.detect_change([2.9, 3.1, 4.0], 0.3))

    def test_detect_decrease_change(self):
        self.assertEqual(True, DataCleaning.detect_change([3.1, 3.0, 2.8], 0.2))

    def test_detect_no_change(self):
        self.assertEqual(False, DataCleaning.detect_change([3.1, 3.1, 3.0], 0.5))

    def test_majority_vote(self):
        self.assertEqual(1, DataCleaning.majority_vote(1, 1, 2))

    def test_stress_level1(self):
        self.assertEqual(1, DataCleaning.detect_stress_level(0.25, 0.5))

    def test_stress_level2(self):
        self.assertEqual(2, DataCleaning.detect_stress_level(0.567, 0.5))

    def test_stress_level0(self):
        self.assertEqual(0, DataCleaning.detect_stress_level(-0.67, 0.5))
