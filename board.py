"""
Describes the board
"""

import numpy as np
from tkinter import *
from move import Move, Moves
from itertools import product


class Board:
    def __init__(self, board=None):
        if board is None:
            self.board = np.zeros((2,26), dtype=np.int32)
            # 0 = home
            # 25 = bar
            self.board[:,24] = [2,2]
            self.board[:,13] = [5,5]
            self.board[:,8] = [3,3]
            self.board[:,6] = [5,5]
        else:
            self.board = board
        
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
        return np.expand_dims(self.board.reshape(-1), axis=0) 
    
    def flip(self):
        return Board(np.flip(self.board, axis=0))

    def step(self, player, move):
        # player = 0 or 1
        other_player = 0 if player == 1 else 1
        next_board = self.board.copy()

        next_board[player,move.point] -= 1
        next_board[player,move.endpoint] += 1
        if move.blot:
            next_board[other_player, 25-move.endpoint] -= 1
            next_board[other_player, 25] += 1 # chcker to bar
        return Board(next_board)

    def _legal_moves_1(self, player, roll):
        # player = 0 or 1
        # roll = 3
        other_player = 0 if player == 1 else 1
        legal_moves = []

        # Checkers on bar
        if self.board[player, 25] != 0: 
            if self.board[other_player, roll] == 0:
                legal_moves.append(Move(25,roll))
            elif self.board[other_player, roll] == 1:
                legal_moves.append(Move(25,roll,blot=True))
        else:
            bearing_off = self.board[player, 7:].sum() == 0
            for i in range(1, 25):
                if self.board[player, i] != 0:
                    if i-roll > 0 and self.board[other_player, 25-i+roll] == 0:
                        legal_moves.append(Move(i,roll))
                    elif i-roll > 0 and self.board[other_player, 25-i+roll] == 1:
                        legal_moves.append(Move(i,roll,blot=True))
                    elif i-roll <= 0 and bearing_off:
                        legal_moves.append(Move(i,roll))
        return legal_moves

    def legal_moves(self, player, rolls):
        legal_moves = []
        if len(rolls) == 2:
            # first order
            lm1 = self._legal_moves_1(player, rolls[0])
            for m1 in lm1:
                next_board = self.step(player, m1)
                lm2 = next_board._legal_moves_1(player, rolls[1])
                if len(lm2) > 0:
                    for m2 in lm2:
                        legal_moves.append(Moves([m1, m2], rolls))
                else:
                    legal_moves.append(Moves([m1], rolls))
            # second order
            lm1 = self._legal_moves_1(player, rolls[1])
            for m1 in lm1:
                next_board = self.step(player, m1)
                lm2 = next_board._legal_moves_1(player, rolls[0])
                if len(lm2) > 0:
                    for m2 in lm2:
                        legal_moves.append(Moves([m1, m2], rolls))
                else:
                    legal_moves.append(Moves([m1], rolls))
        else: # doubles
            legal_moves1 = self._legal_moves_1(player, rolls[0])
            for vm1 in legal_moves1:
                next_board1 = self.step(player, vm1)
                legal_moves2 = next_board1._legal_moves_1(player, rolls[1])
                if len(legal_moves2) > 0:
                    for vm2 in legal_moves2:
                        next_board2 = next_board1.step(player, vm2)
                        legal_moves3 = next_board2._legal_moves_1(player, rolls[2])
                        if len(legal_moves3) > 0:
                            for vm3 in legal_moves3:
                                next_board3 = next_board2.step(player, vm3)
                                legal_moves4 = next_board3._legal_moves_1(player, rolls[3])
                                if len(legal_moves4) > 0:
                                    for vm4 in legal_moves4:
                                        legal_moves.append(Moves([vm1,vm2,vm3,vm4], rolls))
                                else:
                                    legal_moves.append(Moves([vm1,vm2,vm3], rolls))
                        else:
                            legal_moves.append(Moves([vm1,vm2], rolls))
                else:
                    legal_moves.append(Moves([vm1], rolls))
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

    def __str__(self):
        return str(self.board)
        # board_width = 12
        # board_height = 14 ## TODO: case where checkers overlap...
        # board_to_print = np.repeat(".", board_height * board_width).reshape(board_height, -1)
        # for i in range(1,13):
        #     num_checkers = self.board[0,i]
        #     if num_checkers != 0:
        #         for c in range(num_checkers):
        #             board_to_print[board_height-1-c,12-i] = "O"
        #     num_checkers = self.board[1,i]
        #     if num_checkers != 0:
        #         for c in range(num_checkers):
        #             board_to_print[c,12-i] = "X"
        # for i in range(13,25):
        #     num_checkers = self.board[0,i]
        #     if num_checkers != 0:
        #         for c in range(num_checkers):
        #             board_to_print[c,i-13] = "O"
        #     num_checkers = self.board[1,i]
        #     if num_checkers != 0:
        #         for c in range(num_checkers):
        #             board_to_print[board_height-1-c,i-13] = "X"
        # return str(board_to_print)

    def render(self):
        point_width = 32
        board_width = 12*point_width
        board_height = 300

        master = Tk()

        w = Canvas(master, width=board_width, height=board_height)
        w.pack()

        # Draw quadrants 
        w.create_rectangle(0, 0, board_width/2, board_height/2, fill="#222222")
        w.create_rectangle(board_width/2, 0, board_width, board_height/2, fill="#444444")
        w.create_rectangle(0, board_height/2, board_width/2, board_height, fill="#444444")
        w.create_rectangle(board_width/2, board_height/2, board_width, board_height, fill="#444444")
        
        # Draw points
        for x in range(13,25):
            xpnts = [0 + 32*(x-13), 0, 16 + 32*(x-13), 150, 32 + 32*(x-13), 0]
            color = "#AA0000" if x % 2 == 0 else "#55524F"				
            w.create_polygon(xpnts, fill=color)
        for x in range(13,25):
            xpnts = [0 + 32*(x-13), 300, 16 + 32*(x-13), 150, 32 + 32*(x-13), 300]
            color = "#AA0000" if x % 2 != 0 else "#55524F"				
            w.create_polygon(xpnts, fill=color)

        # Draw checkers
        for x in range(13,25):
            xpnts = [0 + 32*(x-13), 0, 16 + 32*(x-13), 150, 32 + 32*(x-13), 0]
            color = "#AA0000" if x % 2 == 0 else "#55524F"				
            w.create_polygon(xpnts, fill=color)
        for x in range(13,25):
            xpnts = [0 + 32*(x-13), 300, 16 + 32*(x-13), 150, 32 + 32*(x-13), 300]
            color = "#AA0000" if x % 2 != 0 else "#55524F"				
            w.create_polygon(xpnts, fill=color)
        # TODO: draw checkers on bar
        mainloop()




