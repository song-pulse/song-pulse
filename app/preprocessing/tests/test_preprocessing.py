import unittest
from app.preprocessing.data_preprocess import DataCleaning


class PreprocessingTest(unittest.TestCase):

    def setUp(self):
        self.preprocess = DataCleaning()

    def test_detect_change(self):
        # TODO override settings either here or in setup?
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
