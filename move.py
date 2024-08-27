"""
Describes a backgammon move
"""
from collections import Counter


class Move:
    def __init__(self, startpoint, endpoint, blot=False):
        # self.point = point
        # self.endpoint = max(point - roll, 0)
        # self.roll = roll
        self.startpoint = startpoint
        self.endpoint = endpoint
        self.blot = blot

    def __eq__(self, other_move):
        if self.startpoint == other_move.startpoint and self.endpoint == other_move.endpoint:
            return True
        else:
            return False

    def __str__(self):
        start = "bar" if self.startpoint == 25 else str(self.startpoint)
        finish = "off" if self.endpoint == 0 else str(self.endpoint)
        blot = "*" if self.blot else ""
        return start + "/" + finish + blot


class Moves:
    def __init__(self, moves, rolls):
        self.moves = moves # list of Move objects
        self.rolls = rolls

    def __eq__(self, other_moves):
        if len(self.moves) != len(other_moves):
            return False
        for move in self.moves:
            is_in_other_moves = False
            for other_move in other_moves:
                if move == other_move:
                    is_in_other_moves = True
                    break
            if not is_in_other_moves:
                return False
        return True

    def __len__(self):
        return len(self.moves)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self.moves):
            i = self.n
            self.n += 1
            return self.moves[i]
        else:
            raise StopIteration

    def __str__(self):
        moves_to_print = ""
        # counts = self.count()
        counts = Counter([str(move) for move in self.moves])
        if len(self.moves) == 0:
            moves_to_print = " (no play)"
        else:
            for move, count in counts.items():
                if count > 1:
                    moves_to_print += " " + move + "(" + str(count) + ")"
                else:
                    moves_to_print += " " + move
        return str(self.rolls[0]) + "-" + str(self.rolls[1]) + ":" + moves_to_print

    