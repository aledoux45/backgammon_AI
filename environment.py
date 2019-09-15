"""
Describes the game of backgammon (i.e the environment)
"""

import numpy as np
from board import Board

class Environment:
    def __init__(self):
        self.board = Board()
        self.board_history = []
        self.moves_history = []
        self.done = False
        self.score = 1
        self.winner = None
        self.loser = None
        self.player_to_move = np.random.randint(2, size=1)[0]

    def reset(self):
        self.board = Board()
        self.board_history = []
        self.moves_history = []
        self.done = False
        self.score = 1
        self.winner = None
        self.loser = None
        self.player_to_move = np.random.randint(2, size=1)[0]

    def step(self, action):
        """
        Moves the environment one step forward (t+=1)
        """
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
                self.score *= 2 # gammon
            if self.board.board[self.loser, 0] == 0 and self.board.board[self.loser, 19:].sum() > 1:
                self.score *= 3 # backgammon
        self.player_to_move = 0 if self.player_to_move == 1 else 1
        return self.board

    def play_game(self, player1, player2, verbose=True):
        """
        Play game between two players
        """
        self.reset()
        cur_board = self.board

        while not self.done:
            if self.player_to_move == 0:
                # print("-- White:")
                roll = player1.roll()
                action = player1.act(cur_board, roll)
            else:
                # print("-- Black:")
                roll = player2.roll()
                action = player2.act(cur_board, roll)

            # print("roll:", roll)
            # print("move:", action)
            self.board_history.append(self.board.copy())
            self.moves_history.append(action)
            cur_board = self.step(action)
            # print(cur_board)

        # Print game
        if verbose:
            if self.winner == 0:
                print("White wins!")
            elif self.winner == 1:
                print("Black wins!")

            # Print game moves
            i=0
            while i < len(self.moves_history):
                if len(self.moves_history) == i+1:
                    print(str(i) + "/ " + str(self.moves_history[i]))
                else:
                    print(str(i) + "/ " + str(self.moves_history[i]) + "\t" + str(self.moves_history[i+1]))
                i+=2
    
    def check_performance(self, player1, player2, num_games):
        """
        Compares performance of player1 vs reference player2
        """
        if player1.player == player2.player:
            raise ValueError("Players have same id in performance check")
        success = 0
        for test_game in range(num_games):
            self.play_game(player1, player2, verbose=False)
            success += self.loser
        return success/num_games