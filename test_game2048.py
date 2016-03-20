from unittest import TestCase
from game2048 import Game2048


class TestGame2048(TestCase):
    def test_get_new_entry(self):
        game = Game2048()
        self.assertIn(game.get_new_entry(), [2, 4])

    def test_check_end(self):
        game = Game2048()
        game.board = [[2,4,8,2],[4,8,2,4],[16,32,64,128],[32,64,128,256]]
        self.assertTrue(game.check_end())

        game.board = [[2,4,8,2],[2,8,2,4],[16,32,64,128],[32,64,128,256]]
        self.assertFalse(game.check_end())

        game.board = [[2,4,8,2],[2,2048,2,4],[16,32,64,128],[32,64,128,256]]
        self.assertTrue(game.check_end())

    def test_make_move(self):
        game = Game2048()
        game.board = [[2,4,8,2],[2,8,2,4],[16,32,64,128],[32,64,128,256]]
        self.assertEqual(game.make_move('w'), 4, 'incorrect score')

    def test_print_board(self):
        game = Game2048()
        game.board = [[2,4,8,2],[2,8,2,4],[16,32,64,128],[32,64,128,2048]]
        game.print_board()
