import numpy as np
from app import crud
from app.schemas.qtable import QTableCreate

EPSILON = 0.5
ALPHA = 0.5
GAMMA = 0.5
NUM_TRAINING = 10


class SongPulseAgent:
    def __init__(self, alpha=ALPHA, gamma=GAMMA, num_training=NUM_TRAINING, epsilon=EPSILON):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.num_training = num_training
        self.states = [0, 1, 2]  # 0: <baseline stress, 1: baseline stress, 2: > baseline stress
        self.actions = [0, 1, 2]  # 0: lower music, 1: stay same, 3: upper music
        self.state = self.states[2]  # init state here but gets overwritten in the tendency fun
        self.timestamp = 23456789234  # bigint, assigned below
        self.run_id = 3
        self.participant_id = 1
        self.feedback = 0
        self.playlist_id = 0
        self.reward = 1  # initially reward is set to 1
        self.new_state = self.state  # initially new_state = state
        self.action = self.actions[1]  # default action is doing nothing (action 1)
        self.n_states = len(self.states)
        self.n_actions = len(self.actions)
        self.Q_table = np.zeros((self.n_states, self.n_actions), dtype=int, order='C')
        print('Q table initial', self.Q_table)

    def get_adaptive_epsilon(self, e):
        """
        compute adaptive epsilon: max(min_epsilon, min(1, 1.0 - np.math.log10((episode + 1) / number_of_states)))
        i.e. more exploration at beginning less at end of training
        :param e: epsilon (exploration parameter), probability at which you take a random action
        :return: epsilon
        """
        if e < (self.num_training / 10):
            self.epsilon = 1.0
        if e > self.num_training * 0.9:
            self.epsilon = 0.0
        return self.epsilon

    def update_q_table(self):
        """
        update Q table entries:  Q(s,a) = Q(s,a) + alpha[R + gamma maxa Q(S',a) -Q(S,A)]
        Q table: all possible states s on y axis and possible actions a on x axis, entry (a,s): expected reward you get
        when being in state s and take action a
        :return:
        """
        self.Q_table[self.state, self.action] += self.alpha * (
                self.reward + self.gamma * np.max(self.Q_table[self.new_state]) - self.Q_table[self.state][self.action])
        return

    def next_state_func(self):
        """
        Transition_matrix[state,action] entry denotes the next state when being in state state and taking action action
        :return: new_state, according to a transition matrix the new state is computed
        """
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
        return self.new_state

    def next_state_with_feedback(self, db_session):
        # TODO: combine these two and use this method instead of next_state_func
        """
        feedback is either 0,1 or 2 (0: bad (too relaxing) , 1:bad (too motivating), 2:good)
        :param db_session:
        :return: new state according to the next state func and user feedback in the app
        """
        self.feedback = self.get_feedback(db_session)  # feedback
        self.new_state = self.next_state_func()  # next state from
        if self.feedback == 0:
            if self.state == 0:
                self.new_state = 0
            else:
                self.new_state = self.state - 1
        if self.feedback == 1:
            if self.state == 2:
                self.new_state = 2
            else:
                self.new_state = self.state + 1
        if self.feedback == 2:
            self.new_state = self.next_state_func()

    def get_feedback(self, db_session):
        tmp = crud.run.get(db_session=db_session, id=self.run_id)
        if len(tmp.results) == 0:
            print('results from run empty -> verdict 1')
            return 1
        verdict = tmp.results[-1].verdict  # this is a number 0,1, or 2 which corresponds to the state
        qtable = self.save_qtable(db_session, data='testdata')
        # TODO: qtable = self.save_qtable(db_session, data=self.Q_table), does not take Q_table
        # TODO: make a get_qtable to get the q_table from the last round
        print('verdict', verdict)
        return verdict

    def save_qtable(self, db_session, data):
        # TODO: make a call to the DB and save the current Q table after every adaption
        """
        saves qtable to db
        :param db_session: current db session
        :param data: qtable (saved as matrix or string)
        :return: qtable which is saved in db
        """
        qtable = crud.qtable.create_with_participant(db_session=db_session, obj_in=QTableCreate(data=data),
                                                     participant_id=self.participant_id)
        return qtable

    def choose_action(self, epsilon=EPSILON):
        if np.random.random() < epsilon:
            # randomly sample explore_rate percent of the time
            print('take random action')
            self.action = np.random.choice(self.actions)
        else:
            # take optimal action
            print('take action from qtable')
            self.action = np.argmax(self.Q_table[self.state])
        return self.action

    def action_state_to_song(self):
        """
        TODO: another function that assigns a spotify link to each playlist_id
        this function takes an action and state(the optimal action for the given state computed and chooses a song
        randomly from one of the 3 spotify playlists)
        :return: song from spotify either the song link or directly play the song here
        """
        # TODO: spotify integration here
        if self.action == 0 & self.state == 0:
            self.playlist_id = 0
        if self.action == 1 & self.state == 0:
            self.playlist_id = 0
        if self.action == 2 & self.state == 0:
            self.playlist_id = 1
        if self.action == 0 & self.state == 1:
            self.playlist_id = 0
        if self.action == 1 & self.state == 1:
            self.playlist_id = 1
        if self.action == 2 & self.state == 1:
            self.playlist_id = 2
        if self.action == 0 & self.state == 2:
            self.playlist_id = 0
        if self.action == 1 & self.state == 2:
            self.playlist_id = 2
        if self.action== 2 & self.state == 2:
            self.playlist_id = 2
        print('playlist_id', self.playlist_id)
        return self.playlist_id

    def get_reward(self):
        """
        reward 0 for an adaption in the wrong direction, 1 for adaption in the right direction and 2 for adaption which
        leads to the right state (i.e state 1)
        :return: reward (how good it is to take a certain action in a certain state)
        """
        if self.new_state == 1:
            self.reward = 3
        elif (self.state == 2 & self.new_state == 0) | (self.state == 0 & self.new_state == 2) | (
                self.state == self.new_state & self.state != 1):
            self.reward = 2
            # case adaption in right direction but not state 1 or state which stays the same
        else:
            # adaption in wrong direction
            self.reward = 1
        return self.reward

    def train(self):
        # simulate execution with rewards that we would get and train the model before running
        for e in range(self.num_training):
            self.epsilon = self.get_adaptive_epsilon(e)
            self.action = self.choose_action(self.state)
            # TODO: here next state should be computed differently
            self.new_state = self.next_state_func()
            print('Train: old state is', self.state)
            print('Train: new state is', self.new_state)
            self.reward = self.get_reward()
            print('reward is', self.reward)
            self.update_q_table()
            print('qtable after update', self.Q_table)
            self.state = self.new_state
            # print('new state', self.state)
        # print('training finished')

    def run(self, number_adaptions):
        """
        take best possible action for a certain state by taking the q matrix computed from training phase
        :param number_adaptions: says for how long, i.e. how many intervals we look at
        for example if we look for 900s and every 30s we want to change the music we have 900/30= 30 num_adaptions
        :return: action to take (go for a motivating, a relaxing or normal song) either 0,1,2
        """
        # TODO: request to server with music like adapt_music(action) where the music gets adapted accordingly
        i = 0
        while i <= number_adaptions:
            best_action_index = self.Q_table[self.state].argmax()  # take the best action for the given current state
            self.action = self.actions[best_action_index]  # take best action
            print('best action for state', self.state, 'is', self.action)
            # TODO DIMITRI: adapt_music(self.action, self.state) --> this function forwarded to server with music
            # TODO Anja: here give a songid and save the already played songs
            # TODO: verdict(rating: in db), timestamp (comes directly from datacleaning), action: int, run_id
            # after a certain time a new state comes in -> new call from the learning_wrapper
            i += 1
        return self.action
        print('run finished for all adaptions')

    def run_with_tendency(self, db_session, tendency, timestamp, run_id, participant_id):
        num_adaptions = 11
        self.state = tendency
        self.timestamp = timestamp
        self.run_id = run_id
        self.participant_id = participant_id
        print('current state', self.state, 'run_id', self.run_id, 'timestamp', self.timestamp,
              'participant_id', self.participant_id)
        print('getFeedback', self.get_feedback(db_session))
        self.train()
        return self.run(num_adaptions)


if __name__ == "__main__":
    agent = SongPulseAgent()
    agent.run_with_tendency(tendency=1, timestamp=1233456789, run_id=3)  # tendency comes from the learning wrapper
    # tendency, timestamp and run_id come from precessing (i.e. learning-wrapper)

