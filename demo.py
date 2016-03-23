from game2048 import Game2048
from DQN_model import Model
import time
import numpy as np

# Start the game.
model = Model()
model.loads('my_model_weights1458523686.h5')
game = Game2048()

# Play 3000 rounds. Definitely ends in 3000 rounds.
for i in range(3000):
    game.print_board()
    if game.check_end():
        print 'Game end'
        exit(0)
    board = np.array(game.view_board())
    state = np.array([board == 2 ** (i+1) for i in range(10)])
    q = model.get_q(state)
    items = sorted(zip(['w', 's', 'a', 'd'], q), key = lambda x: -x[1])
    # Find the optimal feasible action.
    for action, q_value in items:
        if type(game.make_move(action)) == int:
            print 'Take action',action
            break
    time.sleep(1)
