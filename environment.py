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

    def step(self, action):
        # action = Moves object
        if action is None:
            self.player_to_move = 0 if self.player_to_move == 1 else 1
        else:
            self.board = self.board.steps(self.player_to_move, action)
            if not self.board.is_valid():
                raise ValueError("Invalid board")
            if self.board.is_game_over():
                self.done = True 
                self.winner = self.player_to_move
            self.player_to_move = 0 if self.player_to_move == 1 else 1

    def render(self):
        return

