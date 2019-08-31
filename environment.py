"""
Describes the game of backgammon (i.e the environment)
"""

import numpy as np
from board import Board

class Environment:
    def __init__(self):
        self.board = Board()
        self.done = False
        self.winner = None
        self.player_to_move = np.random.randint(2, size=1)[0]

    def reset(self):
        self.board = Board()
        self.done = False
        self.winner = None
        self.player_to_move = np.random.randint(2, size=1)[0]

    def step(self, move):
        # 4-2: 8/4 6/4
        self.board = self.board.step(self.player_to_move, move)
        if self.board[self.player_to_move,:].sum() == 0:
            self.done = True 
            self.winner = self.player_to_move
        self.player_to_move = 0 if self.player_to_move == 1 else 0

    def render(self):
        return

