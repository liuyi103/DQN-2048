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

# random experience replay
choices = ['w', 's', 'a', 'd']
model = Model()
model.loads('my_model_weights1458523686.h5')
game = Game2048()
for i in range(500000):
    game.board = game.get_random_board()
    state1 = model.board_to_state(game.board)
    action = random.choice(choices)
    score = game.make_move(action)
    if score == 'The game has ended!':
        continue
    if score == "nothing happens!":
        score = 0
    state2 = model.board_to_state(game.board)
    model.add_transfer(state1, action, state2, score)

# init everything
game = Game2048()
last_state = None

# First, play some rounds with epsilon = 0.2
epsilon = 0.2
for i in range(10000000):
    if i%1000 == 0:
        print 'round', i
    if i%1000000 == 0:
        model.dumps()
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
        model.add_transfer(state.copy(), action, state.copy(), 0)
    else:
        assert type(ret) == int  # To make sure that the ret is the reward of this action.
        board_next = np.array(game.view_board())
        state_next = np.array([board_next == 2 ** (i+1) for i in range(10)])
        model.add_transfer(state.copy(), action, state_next, ret)

model.dumps()

