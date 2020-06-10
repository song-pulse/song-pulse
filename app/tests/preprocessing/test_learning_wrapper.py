from unittest import TestCase

from app.preprocessing.learning_wrapper import LearningWrapper


class TestLearningWrapper(TestCase):
    def test_calculate_baseline(self):
        self.assertEqual(3.6, LearningWrapper.calculate_baseline(3.2, 2, 4.4))

    def test_calculate_baseline_zero(self):
        self.assertEqual(4.4, LearningWrapper.calculate_baseline(0, 1, 4.4))
