import numpy as np


class MusicMapping:
    def __init__(self, states, actions, state, action):
        self.states = states
        self.actions = actions
        self.state = state
        self.new_state = state
        self.action = action
        self.n_states = len(self.states)
        self.n_actions = len(self.actions)

    def map_state_to_action(self):
        # Transition_matrix is a matrix with states s_i on the y axis and actions a_i on the x axis, the entries (s,a)
        # denote the next state s' when being in state s and taking action a
        Transition_matrix = np.zeros((self.n_states, self.n_actions), dtype=float, order='C')
        Transition_matrix[0, 0] = 0
        Transition_matrix[0, 1] = 0
        Transition_matrix[0, 2] = 1
        Transition_matrix[1, 0] = 0
        Transition_matrix[1, 1] = 1
        Transition_matrix[1, 2] = 2
        Transition_matrix[2, 0] = 1
        Transition_matrix[2, 1] = 2
        Transition_matrix[2, 2] = 2
        print('Transition_matrix', Transition_matrix)
        print('state', self.state, 'action', self.action)
        self.new_state = int(Transition_matrix[self.state, self.action])  # state after applying the corresponding action
        print('new state after transitionmatrix', self.new_state)
        return

    def adapt_music(self):
        print('stress level before adaption', self.state)
        self.map_state_to_action()
        print('stress level after adaption', self.state)

    # TODO: these two methods below are used later for q learning, or an alg that is similar to Q learning
    def map_state_action_to_reward(self):
        # the Reward_matrix is of size sxa and entry at (s,a) defines the reward given when being in state s and taking
        # action a -> this is helpful for q learning later
        # rewards can be either -1 (negative), 0 (neutral) or 1 (positive), goal is to maximize reward
        Reward_matrix = np.zeros((self.n_states, self.n_actions), dtype=float, order='C')
        Reward_matrix[0, 0] = -1
        Reward_matrix[0, 1] = 0
        Reward_matrix[0, 2] = 1
        Reward_matrix[1, 0] = -1
        Reward_matrix[1, 1] = 0
        Reward_matrix[1, 2] = -1
        Reward_matrix[2, 0] = 1
        Reward_matrix[2, 1] = 0
        Reward_matrix[2, 2] = -1
        # TODO: make here a more fine grained rewarding scheme -> i.e. when sth is good vs. very good, bad vs. very bad
        # This prints the reward when being in state self.state and taking action self.action
        print('take action', self.action, 'in state',self.state)
        print('reward', Reward_matrix[self.state, self.action])
        self.state = self.new_state
        print('new state is', self.state)
        return

    def run_with_tendency(self, tendency):
        # tendency comes from learning wrapper
        self.state = tendency
        print('current state', self.state)
        self.adapt_music()
        self.map_state_action_to_reward() # this shows how good taking a certain action in a certain state is


if __name__ == "__main__":
    states = [0, 1, 2]  # 3 different stress levels (below baseline 0, baseline 1, above baseline 2)
    actions = [0, 1, 2]  # 3 different music adaptions (relaxing 0, normal 1, motivating 2)
    # TODO: play with different state and action to see how it behaves
    state = 0  # default state at beginning
    action = 2  # default action at beginning
    agent = MusicMapping(states, actions, state, action)
    agent.run_with_tendency(tendency=0)
