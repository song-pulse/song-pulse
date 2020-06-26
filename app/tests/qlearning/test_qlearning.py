from unittest import TestCase

import numpy as np

from app.api import deps
from app.mltraining.q_learning_music import SongPulseAgent


class TestQlearningMusic(TestCase):

    def test_array_to_string_conversion(self):
        my_array = np.zeros((3, 3), dtype=int, order='C')
        my_string = '000000000'
        self.assertEqual(my_string, SongPulseAgent().array_to_string(data=my_array))

    def test_string_to_array_conversion(self):
        my_string = '000000000'
        my_array = np.zeros((3, 3), dtype=int, order='C')
        np.testing.assert_array_equal(my_array, SongPulseAgent().string_to_array(data=my_string))

    def test_next_state_func(self):
        agent = SongPulseAgent()
        agent.state = 0
        agent.action = 2
        agent.n_states = 3
        agent.n_actions = 3
        self.assertEqual(1, agent.next_state_func())

    def test_get_feedback(self):
        # TODO: setup DB
        agent = SongPulseAgent()
        agent.run_id = 1
        db_session = next(deps.get_db())
        self.assertEqual(3, agent.get_feedback(db_session))
        # TODO: revert DB

    def test_choose_action(self):
        agent = SongPulseAgent()
        agent.actions = [0, 1, 2]
        agent.state = 0
        agent.Q_table = np.zeros((3, 3), dtype=int, order='C')
        self.assertEqual(0, agent.choose_action(epsilon=0))

    def test_get_reward(self):
        agent = SongPulseAgent()
        agent.new_state = 1
        self.assertEqual(3, agent.get_reward())

    # TODO: test run and train method -> test method calls