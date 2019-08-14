"""
Describes the game of backgammon (i.e the environment)
"""

import numpy as np
from board import Board

class Environment:
    def __init__(self):
        self.board = Board()
        self.done = False
        self.player_to_move = np.random.randint(2, size=1)[0]

    def possible_moves(self, roll):
        # roll = np.random.randint(1, 7, size=2)
        moves = []
        if self.board[0,0] != 0: # player has checkers on the bar
            if self.board[roll, 1] <= 1:
                moves.append("bar/"+str(24-roll))
            else:
                return []
        else:
            checkers_positions = np.where(self.board[:,0] != 0)
            for i in checkers_positions:
                if self.board[checkers_positions - roll, 1] == 0:
                    moves.append(str(i)+"/"+str(checkers_positions - roll))
                if self.board[checkers_positions - roll, 1] == 1:
                    moves.append(str(i)+"/"+str(checkers_positions - roll)+"*")
        return moves

    def who_starts(self):
        return np.random.randint(2, size=1)

    def reset(self):
        return

    def step(self, action):
        # 4-2: 8/4 6/4
        return

    def render(self):
        return

