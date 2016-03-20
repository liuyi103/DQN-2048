import numpy as np

class Game2048:
    '''
    This is the class for the game 2048.
    '''
    def get_new_entry(self):
        '''
        :return: a new entry 2 / 4 according to the probability
        '''
        if np.random.random() < self.probability2:
            return 2
        return 4

    def __init__(self):
        self.board = [[0 for i in range(4)] for j in range(4)]
        self.score = 0
        self.probability2 = 0.8  # For a new number, with this probability to be 2, otherwise 4.
        self.entries = [(i, j) for i in range(4) for j in range(4)]

        # initilize the board
        x1, y1, x2, y2 = np.random.randint(0, 4, 4)
        while x1 == x2 and y1 == y2:
            x1, y1, x2, y2 = np.random.randint(0, 4, 4)
        self.board[x1][y1] = self.get_new_entry()
        self.board[x2][y2] = self.get_new_entry()

    def view_board(self):
        '''
        :return: the current board
        '''
        return self.board

    def check_end(self):
        '''
        :return: whether the game is end.
        '''
        # if 2048 has been obtained, the game finish.
        for row in range(4):
            for col in range(4):
                if self.board[row][col] == 2048:
                    return True

        # if there is still a blank or a feasible move, the game goes on.
        for row in range(4):
            for col in range(4):
                if self.board[row][col] == 0:
                    return False
                for dx, dy in [(0, 1), (1, 0)]:
                    if row + dx < 4 and col + dy < 4 and self.board[row][col] == self.board[row + dx][col + dy]:
                        return False

        # Otherwise, lose the game!
        return True

    def make_move(self, direction):
        '''
        Make move on the board and add a new entry. in the end.
        First, judge end of game and valid.
        Second, make moves, during this process, after combination entries may be temporary be negative.
        Third, update score
        Forth, add a new entry.
        :param direction:'w', 's', 'a', 'd' for up, down, left, right
        :return: the score increment or a message
        '''
        # First Step
        if self.check_end():
            return 'The game has ended!'

        # Map direction to the deltas
        dir_map = {'w': (-1, 0), 's': (1, 0), 'a': (0,-1), 'd': (0, 1)}
        try:
            direction = dir_map[direction]
        except:
            return 'incorrect direction'

        # Second step
        feasible_move = False
        dx, dy = dir
        add_score = 0
        for x in range(4)[::-dx]:
            for y in range(4)[::-dy]:
                # empty entry
                if self.board[x][y] == 0:
                    continue

                nx, ny = x, y  # new x, new y

                # If empty, push forward.
                while (nx + dx, ny + dy) in self.entries and self.board[nx + dx][ny + dy] == 0:
                    nx, ny = nx + dx, ny + dy
                tmp = self.board[x][y]
                self.board[x][y] = 0
                self.board[nx][ny] = tmp

                # If the values are the same, combine them
                if (nx + dx, ny + dy) in self.entries and self.board[nx + dx][ny + dy] == self.board[nx][ny]:
                    add_score += self.board[nx][ny] * 2
                    self.board[nx + dx][ny + dy] *= -2
                    self.board[nx][ny] = 0

                # if moved feasible
                if self.board[x][y] == 0:
                    feasible_move = True

        # The current move changes nothing, return
        if not feasible_move:
            return "nothing happens!"

        # make the values back to positive
        for x, y in self.entries:
            self.board[x][y] = abs(self.board[x][y])

        # Third step
        self.score += add_score

        # Fotrh step
        empty_entries = [(x, y) for x, y in self.entries if self.board[x][y] == 0]
        k = np.random.choice(range(len(empty_entries)))
        x, y = empty_entries[k]
        self.board[x][y] = self.get_new_entry()

        return add_score

    def print_board(self):
        print 'Score: %d' % self.score
        for i in range(4):
            print '%8d%8d%8d%8d' % self.board[i]

