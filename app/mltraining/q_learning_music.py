import numpy as np


def main():
    print('hello world')  # just for testing purpose
    # TODO: 1) read in data (HRV/EDA or both)
    alpha = 0.5  # between 0 and 1
    gamma = 0.5  # sth between 0 and 1
    states = [0, 1, 2]  # 3 stress states: 0 means below baseline stress, 1 baseline stress, 2 above baseline stress
    actions = [0, 1, 2]  # 3 different actions: lower music, stay same, upper music
    rewards = [-1, 0, 1]  # possible rewards (the bigger the reward the better)
    Q_table = np.zeros((len(states), len(actions)))
    print('Q_table', Q_table)
    set_parameters(alpha, gamma, states, actions, rewards)
    # TODO: define userrating mapping and how to integrate (scores fom 1 to 5 --> mapped to rewards) TODO: define
    #  timesteps at which we get the data -> either HRV/EDA need to be combined and need to be same TODO: for
    #   simplicity just take one of the two parameters and fix timesteps at which we get the data TODO: 2) set
    #    parameters (alpha, gamma, ...) TODO: 3) define stateset, actionset, transitionfunction etc. TODO: 3) define
    #     update steps for actions, policy etc (as we have to build a new env, not like in gym) TODO: 4) run q
    #      learning for normal data TODO 5) run q learning for feedback TODO: 6) define episode and terminal state
    #       for alg -> an episode is defined through a cerain timestep TODO the terminal state is when the
    #        stresslevel stays at the perfect level or when all data is finished (we have gone through)


def read_in_data():
    return


def set_parameters(alpha, gamma, states, actions, rewards):
    alpha = alpha
    gamma = gamma
    a0 = actions[1]  # default action is doing nothing (action 1)
    s0 = states[1]  # default state is baseline stress (state 1)
    r0 = rewards[1]  # default reward is 0


def update_q_table():
    # TODO: see algorithm q learning
    # q table is a table with all possible states s on the y axis and the possible actions a on the x axis
    # the entries at (a,s) denote the expected reward you get when being in state s and take action a
    return


def next_state(state):
    # TODO: input is a given stte and this function returns the nextstate (transitionfunction)
    return


def choose_action():
    return


def run__q_learning():
    return


if __name__ == "__main__":
    main()
