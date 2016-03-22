from game2048 import Game2048
from DQN_model import Model
#
# modeL = Model()
# model.loads()
# print 'called'
# game = Game2048()
# for i in range(3000):
#     if game.check_end():
#         return game.score
#     board = np.array(game.view_board())
#     state = np.array([board == 2 ** (i+1) for i in range(10)])
#     q = model.get_q(state)
#     items = sorted(zip(['w', 's', 'a', 'd'], q), key = lambda x: -x[1])
#     for action, q_value in items:
#         if type(game.make_move(action)) == int:
#             break
# return game.score
