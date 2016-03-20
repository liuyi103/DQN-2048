# This code implementss DQN for the game 2048.
# Unlike the original paper, we directly use the numbers in the grids as inputs.
# The input is consists of 10 frames. The i-th frame is a board for board[i][j] == 2 ** i, which is binary.
# The structure of the network is as follows.
#
#
#

from game2048 import Game2048
import numpy as np
import random
from DQN_model import Model

# policy: with epsilon probabilty: random, otherwise: the best choice.
experiences = []  # ech entry: state1, action, state2, reward

# init everything
game = Game2048()
last_state = None
choices = ['w', 's', 'a', 'd']
model = Model()

# First, play some rounds with epsilon = 0.5
epsilon = 0.5
for i in range(100000):
    if game.check_end():
        game = Game2048()
    board = np.array(game.view_board())
    state = np.array([board == 2 ** (i+1) for i in range(10)])
    q = model.get_q(state)
    if np.random.random() < epsilon:
        action = random.choice(choices)
    else:
        action = choices[max(range(4), key = lambda x: q[x])]
    ret = game.make_move(action)
    if ret == 'nothing happens!':
        experiences.append((state.copy(), action, state.copy(), 0))
    else:
        assert type(ret) == int  # To make sure that the ret is the reward of this action.
        board_next = np.array(game.view_board())
        state_next = np.array([board_next == 2 ** (i+1) for i in range(10)])
        experiences.append((state.copy(), action, state_next, ret))
    model.add_transfer(*experiences[-1])

model.dumps()
