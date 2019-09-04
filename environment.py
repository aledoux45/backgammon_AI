"""
Describes the game of backgammon (i.e the environment)
"""

import numpy as np
from board import Board

class Environment:
    def __init__(self):
        self.board = Board()
        self.done = False
        self.score_scale = 1
        self.winner = None
        self.loser = None
        self.player_to_move = np.random.randint(2, size=1)[0]

    def reset(self):
        self.board = Board()
        self.done = False
        self.winner = None
        self.player_to_move = np.random.randint(2, size=1)[0]

    def step(self, action):
        # action = Moves object
        for move in action:
            self.board = self.board.step(self.player_to_move, move)
        if not self.board.is_valid():
            raise ValueError("Invalid board")
        if self.board.is_game_over():
            self.done = True 
            self.winner = self.player_to_move
            self.loser = 0 if self.winner == 1 else 1
            if self.board.board[self.loser, 0] == 0:
                self.score_scale *= 2 # gammon
            if self.board.board[self.loser, 0] == 0 and self.board.board[self.loser, 19:].sum() > 1:
                self.score_scale *= 3 # backgammon
        self.player_to_move = 0 if self.player_to_move == 1 else 1
        return self.board
