'''
This file is to play 2048 by human.
'w', 's', 'a', 'd' for up, down, left and right
'''
from game2048 import Game2048

if __name__ == '__main__':
    game = Game2048()
    while not game.check_end():
        game.print_board()
        action = raw_input()
        game.make_move(action)
    print 'Game ends!'