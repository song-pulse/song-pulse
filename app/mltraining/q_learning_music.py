import numpy as np

# alpha, gamma and epsilon are values between 0 and 1
EPSILON = 0.5  # epsilon near 1 much exploration, epsilon near 0 more strategy among the q learning -> use adaptive one
ALPHA = 0.5
GAMMA = 0.5
NUM_TRAINING = 10


class SongPulseAgent:
    def __init__(self, alpha=ALPHA, gamma=GAMMA, num_training=NUM_TRAINING, epsilon= EPSILON):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.num_training = num_training
        self.states = [0, 1, 2]  # 0 means below baseline stress, 1 baseline stress, 2 above baseline stress
        self.actions = [0, 1, 2]  # 3 different actions: lower music, stay same, upper music
        self.rewards = [-1, 0, 1]  # possible rewards (the bigger the reward the better)
        self.reward = self.rewards[1]  # default reward is 0
        self.state = self.states[1]  # default state is baseline stress (state 1)
        self.new_state = self.state  # initially new_state = state
        self.action = self.actions[1]  # default action is doing nothing (action 1)
        print('states len', (len(self.states)))
        self.n_states = len(self.states)
        self.n_actions = len(self.actions)
        self.Q_table = np.zeros((self.n_states, self.n_actions), dtype=int, order='C')
        print('Q_table', self.Q_table)

    def get_adaptive_epsilon(self, e):
        # return max(min_epsilon, min(1, 1.0 - np.math.log10((episode + 1) / number_of_states)))
        if e < (self.num_training / 10):
            return 1.0
        if e > self.num_training * 0.9:
            return 0.0
        return EPSILON

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
        Transition_matrix = np.zeros((self.n_states, self.n_actions), dtype=int, order='C')
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
        print('new state', new_state)
        return new_state

    def choose_action(self, epsilon=EPSILON):
        if np.random.random() < epsilon:
            # randomly sample explore_rate percent of the time
            return np.random.choice(self.actions)
        else:
            # take optimal action
            return np.argmax(self.Q_table[self.state])

    def train(self):
        # simulate execution with rewards that we would get and train the model before running
        for e in range(self.num_training):
            done = False

            while not done:
                print('old state', self.state)
                self.epsilon = self.get_adaptive_epsilon(e)
                self.action = self.choose_action(self.state)
                self.new_state = self.next_state_func()  # TODO: look at this as we get the next state also from
                # measure, this is only what we expect, so maybe get next_state should go to the server -> not
                # possible due to real time issue? not predictable -> learn with already there data
                reward = self.Q_table[self.state, self.action]
                print('reward', reward)
                # TODO: define reward, retrieve done variable, and new_state
                self.update_q_table(self.state, self.action, reward, new_state=self.new_state)
                self.state = self.new_state
                print('new state', self.state)
            print('training finished')

    def run(self, num_adaptions):
        # this runs the problem by taking the best possible action for a certain state by taking the q matrix
        # computed from the training phase
        # self.state is the incoming stress state the person is in
        # request to server with music like adapt_music(action) where the music gets adapted accordingly
        # num_adaptions denotes
        i = 0
        while i <= num_adaptions:
            best_action_index = self.Q_table[self.state].argmax()  # take the best action for the given current state
            self.action = self.actions[best_action_index]  # take best action
            print('best action for state', self.state, 'is', self.action)
            # TODO: adapt_music(self.action, self.state) --> this function forwarded to server with music
            # after a certain time a new state comes in
            i += 1
        print('run finished for all adaptions')


if __name__ == "__main__":
    agent = SongPulseAgent()
    agent.train()  # this fills the Q table in order for it to get an optimal policy
    num_adaptions = 200  # this number says for how long, i.e. how many intervals we look at
    # for example if we look for 900s and every 30s we want to change the music we have 900/30= 30 num_adaptions
    agent.run(num_adaptions)
# TODO: difference to other q learning algs -> the state should not get updated in the run phase as the state comes from
# our measurements not and cannot be fully determined by us
