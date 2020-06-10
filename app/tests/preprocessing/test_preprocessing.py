from unittest import TestCase
from app.preprocessing.data_preprocess import DataCleaning


class PreprocessingTest(TestCase):

    def setUp(self):
        self.preprocess = DataCleaning()

    def test_detect_change(self):
        # TODO override settings either here or in setup?
        self.assertEqual(True, False)
