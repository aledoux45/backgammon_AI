"""
Describes the board
"""

import numpy as np
from move import Move, Moves
from itertools import product


class Board:
    def __init__(self, board=None):
        if board is None:
            # The board is represented by a 2x26 array
            # 0 = home
            # 25 = bar
            self.board = np.zeros((2,26), dtype=np.int32)
            # initial positions
            self.board[:,24] = [2,2]
            self.board[:,13] = [5,5]
            self.board[:,8] = [3,3]
            self.board[:,6] = [5,5]
        else:
            self.board = board
    
    def reset(self):
        self.board = np.zeros((2,26), dtype=np.int32)
        self.board[:,24] = [2,2]
        self.board[:,13] = [5,5]
        self.board[:,8] = [3,3]
        self.board[:,6] = [5,5]

    def is_game_over(self):
        if self.board[0,1:].sum() == 0 or self.board[1,1:].sum() == 0:
            return True
        else:
            return False

    def is_valid(self):
        if self.board[0,:].sum() != 15:
            print("Wrong number of checkers for White")
            return False
        if self.board[1,:].sum() != 15:
            print("Wrong number of checkers for Black")
            return False
        for i in range(1, 25):
            if self.board[0, i] != 0 and self.board[1,25-i] != 0:
                print("Two players on same point:", i)
                return False
        for i in range(26):
            if self.board[0, i] < 0 or self.board[1, i] < 0:
                print("Negative number of checkers")
                return False
        return True

    def copy(self):
        return Board(self.board)
        
    def flat(self):
        return self.board.reshape(1,52)
    
    def flip(self):
        return Board(np.flip(self.board, axis=0))

    def step(self, player, move):
        """
        Gives the next board after move
        player = 0 or 1
        move = Move or Moves object
        """
        other_player = 0 if player == 1 else 1
        next_board = self.board.copy()

        if isinstance(move, Move):
            next_board[player,move.startpoint] -= 1
            next_board[player,move.endpoint] += 1
            if move.blot:
                next_board[other_player, 25 - move.endpoint] -= 1
                next_board[other_player, 25] += 1 
        else:
            for m in move:
                next_board[player,m.startpoint] -= 1
                next_board[player,m.endpoint] += 1
                if m.blot:
                    next_board[other_player, 25 - m.endpoint] -= 1
                    next_board[other_player, 25] += 1 

        return Board(next_board)

    def legal_moves_1(self, player, roll):
        """
        Gives the legal move for 1 roll
        player = 0 or 1
        roll = int in [1;6]
        output = List[Move]
        """
        other_player = 0 if player == 1 else 1
        legal_moves = []

        # Checkers on bar
        if self.board[player, 25] != 0:
            endpoint = 25 - roll
            if endpoint > 0 and self.board[other_player, 25-endpoint] == 0:
                legal_moves.append(Move(25, endpoint))
            elif endpoint > 0 and self.board[other_player, 25-endpoint] == 1:
                legal_moves.append(Move(25, endpoint, blot=True))
        else:
            bearing_off = np.sum(self.board[player, 7:]) == 0
            for point in range(24, 0, -1):
                if self.board[player, point] != 0:
                    endpoint = point - roll
                    if endpoint > 0 and self.board[other_player, 25-endpoint] == 0:
                        legal_moves.append(Move(point, endpoint))
                    elif endpoint > 0 and self.board[other_player, 25-endpoint] == 1:
                        legal_moves.append(Move(point, endpoint, blot=True))
                    elif endpoint <= 0 and bearing_off:
                        legal_moves.append(Move(point, 0))
        return legal_moves

    def legal_moves_n(self, player, rolls):
        """
        Gives the legal moves for several rolls of dice IN THE ORDER GIVEN
        player = 0 or 1
        rolls = List[int] in [1;6]
        output = List[List[Move]]
        """
        if len(rolls) == 0:
            return [ [] ]
        
        l_moves1 = self.legal_moves_1(player, rolls[0])
        if len(l_moves1) == 0:
            return [ [] ]
        if len(rolls) == 1:
            return [[m] for m in l_moves1]
        
        legal_moves = []
        for move in l_moves1:
            next_board = self.step(player, move)
            next_moves = next_board.legal_moves_n(player, rolls[1:])
            legal_moves += [[move] + moves for moves in next_moves]
        
        return legal_moves

    def legal_moves(self, player, rolls):
        # returns a list of Moves object
        if len(rolls) == 2:
            # order can matter
            legal_moves1 = self.legal_moves_n(player, [rolls[0],rolls[1]] )
            legal_moves2 = self.legal_moves_n(player, [rolls[1],rolls[0]] )
            legal_moves = legal_moves1 + legal_moves2
        else: 
            # roll doubles
            legal_moves = self.legal_moves_n(player, rolls)

        legal_moves = [Moves(m, rolls) for m in legal_moves]
        # only keep unique moves
        unique_legal_moves = []
        for lm in legal_moves:
            lm_found = False
            for ulm in unique_legal_moves:
                if lm == ulm:
                    lm_found = True
                    break
            if not lm_found:
                unique_legal_moves.append(lm)
        return unique_legal_moves

    def render_ui(self):
        board_width = 13
        board_height = 14 ## TODO: case where checkers overlap...
        board_to_print = np.repeat(".", board_height * board_width).reshape(board_height, -1)
        for i in range(1,13):
            num_checkers = self.board[0,i]
            if num_checkers != 0:
                for c in range(num_checkers):
                    board_to_print[board_height-1-c,12-i] = "O"
            num_checkers = self.board[1,i]
            if num_checkers != 0:
                for c in range(num_checkers):
                    board_to_print[c,12-i] = "X"
        for i in range(13,26):
            num_checkers = self.board[0,i]
            if num_checkers != 0:
                for c in range(num_checkers):
                    board_to_print[c,i-13] = "O"
            num_checkers = self.board[1,i]
            if num_checkers != 0:
                for c in range(num_checkers):
                    board_to_print[board_height-1-c,i-13] = "X"
        return board_to_print

    def __str__(self):
        # return str(self.render_ui())
        return str(self.board)




