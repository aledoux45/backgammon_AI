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
        self.player_to_move = np.random.randint(2, size=1)[0]

        # Result
        self.game_over = False
        self.score = 1
        self.winner = None
        self.loser = None

    def reset(self):
        self.board = Board()
        self.board_history = []
        self.moves_history = []
        self.player_to_move = np.random.randint(2, size=1)[0]
    
        # Result
        self.game_over = False
        self.score = 1
        self.winner = None
        self.loser = None

    def step(self, action):
        """
        Moves the environment one step forward (t+=1)
        action = Moves object
        """
        for move in action:
            self.board = self.board.step(self.player_to_move, move)
        
        if not self.board.is_valid():
            raise ValueError("Invalid board")
        
        if self.board.is_game_over():
            self.game_over = True 
            # Who won?
            if self.board.board[0,1:].sum() == 0:
                self.winner = 0
                self.loser = 1
            else:
                self.winner = 1
                self.loser = 0
            # Gammon
            if self.board.board[self.loser, 0] == 0:
                self.score *= 2
            # Backgammon
            elif self.board.board[self.loser, 0] == 0 and np.sum(self.board.board[self.loser, 19:]) > 1:
                self.score *= 3
        self.player_to_move = 0 if self.player_to_move == 1 else 1
        return self.board

    def play_game(self, player1, player2, verbose=True):
        """
        Play game between two players
        player1 = 0
        player2 = 1
        action = Moves object
        """
        self.reset()
        cur_board = self.board
        if player1.player != 0 or player2.player != 1:
            raise ValueError("Must have Player 0 and 1")

        while not self.game_over:
            if self.player_to_move == 0:
                rolls = player1.roll()
                action = player1.act(cur_board, rolls)
                if verbose:
                    print("-- White:")
            else:
                
                rolls = player2.roll()
                action = player2.act(cur_board, rolls)
                if verbose:
                    print("-- Black:")

            self.board_history.append(self.board.copy())
            self.moves_history.append(action)
            cur_board = self.step(action)
            if verbose:
                print("roll:", rolls)
                print("move:", action)
                print(cur_board)

        # Print game
        if verbose:
            if self.winner == 0:
                print("White wins!")
            elif self.winner == 1:
                print("Black wins!")

            # Print game moves
            print()
            print("------ GAME SUMMARY ------")
            i = 0
            while i < len(self.moves_history):
                if len(self.moves_history) == i+1:
                    print(str(i) + "/ " + str(self.moves_history[i]))
                else:
                    print(str(i) + "/ " + str(self.moves_history[i]) + "\t" + str(self.moves_history[i+1]))
                i += 2
    
    def check_performance(self, player1, player2, num_games):
        """
        Compares performance of player1 vs reference player2
        """
        if player1.player == player2.player:
            raise ValueError("Players have same id in performance check")
        success = 0
        for test_game in range(num_games):
            self.play_game(player1, player2, verbose=False)
            if self.winner == player1.player:
                success += 1
        return success / num_games