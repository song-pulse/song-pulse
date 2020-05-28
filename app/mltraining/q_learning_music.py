import numpy as np

from app.main import get_run

# alpha, gamma and epsilon are values between 0 and 1
EPSILON = 0.5  # epsilon near 1 much exploration, epsilon near 0 more strategy among the q learning -> use adaptive one
ALPHA = 0.5
GAMMA = 0.5
NUM_TRAINING = 10


class SongPulseAgent:
    def __init__(self, alpha=ALPHA, gamma=GAMMA, num_training=NUM_TRAINING, epsilon=EPSILON):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.num_training = num_training
        self.states = [0, 1, 2]  # 0 means below baseline stress, 1 baseline stress, 2 above baseline stress
        self.actions = [0, 1, 2]  # 3 different actions: lower music, stay same, upper music
        self.state = self.states[2]  # init state here but gets overwritten in the tendency fun
        self.timestamp = 23456789234  # bigint, assigned below
        self.run_id = 3
        self.feedback = 0
        # self.state now comes from tendency and is assigned below
        self.reward = 1  # initially reward is set to 1
        self.new_state = self.state  # initially new_state = state
        self.action = self.actions[1]  # default action is doing nothing (action 1)
        self.n_states = len(self.states)
        self.n_actions = len(self.actions)
        self.Q_table = np.zeros((self.n_states, self.n_actions), dtype=int, order='C')

    def get_adaptive_epsilon(self, e):
        # return max(min_epsilon, min(1, 1.0 - np.math.log10((episode + 1) / number_of_states)))
        if e < (self.num_training / 10):
            self.epsilon = 1.0
        if e > self.num_training * 0.9:
            self.epsilon = 0.0
        return self.epsilon

    def update_q_table(self):
        # update Q table: Q(s,a) = Q(s,a) + alpha[R + gamma maxa Q(S',a) -Q(S,A)]
        # q table is a table with all possible states s on the y axis and the possible actions a on the x axis
        # the entries at (a,s) denote the expected reward you get when being in state s and take action a
        self.Q_table[self.state, self.action] += self.alpha * (
                self.reward + self.gamma * np.max(self.Q_table[self.new_state]) - self.Q_table[self.state][self.action])
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
        self.new_state = Transition_matrix[self.state, self.action]
        # print('new state', self.new_state)
        return self.new_state

    def next_state_with_feedback(self):
        self.feedback = self.get_feedback()  # feedback
        self.new_state = self.next_state_func()  # next state from
        # TODO: combine these two and use this method instead of next_state_func


    def get_feedback(self):
        # use getRun async def get_run(*, run_id: int, db: Session = Depends(get_db)):
        #  <-- from this object we need results['verdict'] (see main.py)
        # TODO: updateResult needed?
        # TODO: get run_id and timestamp from preprocessing, as well as song_id
        # TODO: take the results with the same timestamp as we have -> timestamp from now look at the last one (find the biggest timestamp that is smaller than the current)
        tmp = await get_run(self.run_id)
        verdict = tmp.results.last['verdict']  # this is a number 0,1, or 2 which corresponds to the state
        print('verdict', verdict)
        # async def get_run(*, run_id: int, db: Session = Depends(get_db)): <-- from this object we need results['verdict']
        return verdict

    def save_qtable(self):
        # TODO: make a call to the DB and save the current Q table after every adaption
        # TODO: discuss with dimitri, where in the db this self.Q_table should go
        return

    def choose_action(self, epsilon=EPSILON):
        if np.random.random() < epsilon:
            # randomly sample explore_rate percent of the time
            self.action = np.random.choice(self.actions)
        else:
            # take optimal action
            self.action = np.argmax(self.Q_table[self.state])
            # print(' HALLO qtable[self.state]', self.Q_table[self.state])
            # print('action', self.action)
        return self.action

    def get_reward(self):
        # TODO: discuss how rewarding scheme should be done
        # if new_state is better than state positive reward, else neg reward -> state s is best
        # positive if from s0 to s1 or from s2 to s1
        # reward 0 for an adaption in the wrong direction, 1 for an adaption in the right direction and
        # 2 for an adaption which leads to the right state (i.e. state 1)
        if self.new_state == 1:
            self.reward = 3
        elif (self.state == 2 & self.new_state == 0) | (self.state == 0 & self.new_state == 2) | (
                self.state == self.new_state & self.state != 1):
            self.reward = 2
            # TODO ensure that self.state is the old state -> otw give oldstate as an argument
            # case adaption in right direction but not state 1 or state which stays the same
        else:
            # adaption in wrong direction
            self.reward = 1
        return self.reward

    def train(self):
        # simulate execution with rewards that we would get and train the model before running
        for e in range(self.num_training):
            done = False

            while not done:
                # print('old state', self.state)
                self.epsilon = self.get_adaptive_epsilon(e)
                self.action = self.choose_action(self.state)
                # TODO: here next state should be computed differently
                self.new_state = self.next_state_func()
                self.reward = self.get_reward()
                # print('reward is', self.reward)
                self.update_q_table()
                # print('qtable after update', self.Q_table)
                self.state = self.new_state
                # print('new state', self.state)
            # print('training finished')

    def run(self, number_adaptions):
        # this runs the problem by taking the best possible action for a certain state by taking the q matrix
        # computed from the training phase
        # self.state is the incoming stress state the person is in
        # request to server with music like adapt_music(action) where the music gets adapted accordingly
        # num_adaptions denotes
        i = 0
        while i <= number_adaptions:
            best_action_index = self.Q_table[self.state].argmax()  # take the best action for the given current state
            self.action = self.actions[best_action_index]  # take best action
            print('best action for state', self.state, 'is', self.action)
            # TODO DIMITRI: adapt_music(self.action, self.state) --> this function forwarded to server with music
            # TODO Anja: here give a songid and save the already played songs
            # TODO: verdict(rating: in db), timestamp (comes directly from datacleaning), action, action: int
            # TODO: mapping from int to string --> 0-> 'low' etc.
            # TODO: runid
            # after a certain time a new state comes in
            i += 1
        print('run finished for all adaptions')

    def run_with_tendency(self, tendency, timestamp, run_id):
        # tendency comes from learning wrapper and num_adaptions is just given here fixed
        self.state = tendency
        self.timestamp = timestamp
        self.run_id = run_id
        print('current state', self.state, 'self.run_id', self.run_id, 'self.timestamp', self.timestamp)
        self.train()
        return self.run(11)


if __name__ == "__main__":
    agent = SongPulseAgent()
    # agent.train()  # this fills the Q table in order for it to get an optimal policy
    agent.run_with_tendency(tendency=1, timestamp=1233456789, run_id=3)  # tendency comes from the learning wrapper
    # TODO: here tendency, timestamp and run_id come from data preprocess and stream
    num_adaptions = 11  # this number says for how long, i.e. how many intervals we look at
    # for example if we look for 900s and every 30s we want to change the music we have 900/30= 30 num_adaptions
    # TODO Dimitri: crud.run.create()
    agent.run(number_adaptions=num_adaptions)
# TODO: difference to other q learning algs -> the state should not get updated in the run phase as the state comes from
# our measurements not and cannot be fully determined by us

# TODO: define training and run data -> with the training data we now and get the next state and reward -> with the
# run data we don't but we just act according to the created policy

# TODO: later compare with basic strategy music mapping
