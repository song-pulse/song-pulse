import numpy as np

# alpha, gamma and epsilon are values between 0 and 1
EPSILON = 0.5


class SongPulseAgent:
    def __init__(self, alpha=0.5, gamma=0.5, num_episodes=10):
        self.alpha = alpha
        self.gamma = gamma
        self.num_episodes = num_episodes
        self.states = [0, 1, 2]  # 0 means below baseline stress, 1 baseline stress, 2 above baseline stress
        self.actions = [0, 1, 2]  # 3 different actions: lower music, stay same, upper music
        self.rewards = [-1, 0, 1]  # possible rewards (the bigger the reward the better)
        self.reward = self.rewards[1]  # default reward is 0
        self.state = self.states[1]  # default state is baseline stress (state 1)
        self.action = self.actions[1]  # default action is doing nothing (action 1)
        print('states len', (len(self.states)))
        self.n_states = len(self.states)
        self.n_actions = len(self.actions)
        self.Q_table = np.zeros((self.n_states, self.n_actions), dtype=float, order='C')
        print('Q_table', self.Q_table)

    def update_q_table(self, state, action, reward, new_state):
        # update Q table: Q(s,a) = Q(s,a) + alpha[R + gamma maxa Q(S',a) -Q(S,A)]
        # q table is a table with all possible states s on the y axis and the possible actions a on the x axis
        # the entries at (a,s) denote the expected reward you get when being in state s and take action a
        self.Q_table[state, action] += self.alpha * (
                reward + self.gamma * np.max(self.Q_table[new_state]) - self.Q_table[state][action])
        return

    def next_state_func(self):
        # transition function: input is a given state and action and this function returns the next_state when taking
        # action transition table -> position state,action entry denotes next state
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
        print('transition matrix', Transition_matrix)
        new_state = Transition_matrix[self.state, self.action]
        return new_state

    def get_new_reward(self):
        # shows return for taking step from (s,a) to (s',a)
        # make a reward -state-action matrix for this
        # TODO: self.reward =
        return self.reward

    def choose_action(self, epsilon=EPSILON):
        if np.random.random() < epsilon:
            # randomly sample explore_rate percent of the time
            return np.random.choice(self.actions)
        else:
            # take optimal action
            return np.argmax(self.Q_table[self.state])

    def train(self):
        # simulate execution with rewards that we would get and train the model before running
        for e in range(self.num_episodes):
            done = False

            while not done:
                action = self.choose_action(self.state)
                new_state = self.next_state_func()
                reward = self.get_new_reward()
                # TODO: define reward, retrieve done variable, and new_state
                self.update_q_table(self.state, action, reward, new_state=new_state)
                self.state = new_state
            print('training finished')

    def run(self):
        # TODO:
        return


if __name__ == "__main__":
    agent = SongPulseAgent()
    agent.train()
    agent.run()
