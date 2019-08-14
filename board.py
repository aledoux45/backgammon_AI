"""
Describes the board
"""

import numpy as np
from tkinter import *
from move import Move


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

    def _next_board(self, player, move):
        # player = 0 or 1
        other_player = 0 if player == 1 else 1

    def valid_moves_1(self, player, roll):
        # player = 0 or 1
        # roll = 3
        other_player = 0 if player == 1 else 1
        valid_moves = []
        if self.board[player, 0] != 0: # checkers on bar
            if self.board[other_player, roll] == 0:
                valid_moves.append(Move(25,roll))
            elif self.board[other_player, roll] == 1:
                valid_moves.append(Move(25,roll,blot=True))
            return valid_moves

        for i in range(1, 25):
            if self.board[player, i] != 0:
                return

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


    def __str__(self):
        return str(self.board)

