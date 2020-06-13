from unittest import TestCase
import numpy as np
from app import crud
from app.api import deps

from app.mltraining.q_learning_music import SongPulseAgent


class TestQlearningMusic(TestCase):

    def test_array_to_string_conversion(self):
        my_array = np.zeros((3, 3), dtype=int, order='C')
        my_string = '000000000'
        self.assertEqual(my_string, SongPulseAgent.array_to_string(self, data=my_array))

    def test_string_to_array_conversion(self):
        my_string = '000000000'
        my_array = np.zeros((3, 3), dtype=int, order='C')
        np.testing.assert_array_equal(my_array, SongPulseAgent.string_to_array(self, data=my_string))

    def test_next_state_func(self):
        new_state = 1
        self.state = 0
        self.action = 2
        self.n_states = 3
        self.n_actions = 3
        self.assertEqual(new_state, SongPulseAgent.next_state_func(self))

    def test_get_feedback(self):
        self.run_id = 1
        db_session = next(deps.get_db())
        verdict = 3
        self.assertEqual(verdict, SongPulseAgent.get_feedback(self,db_session))

    def test_choose_action(self):
        self.actions = [0, 1, 2]
        self.state = 0
        self.Q_table = np.zeros((3, 3), dtype=int, order='C')
        action = 0
        self.assertEqual(action, SongPulseAgent.choose_action(self, epsilon=0))

    def test_get_reward(self):
        self.new_state = 1
        reward = 3
        self.assertEqual(reward, SongPulseAgent.get_reward(self))

    # TODO: test run and train method -> test method calls