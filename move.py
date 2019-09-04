"""
Describes a backgammon move
"""


class Move:
    def __init__(self, point, roll, blot=False):
        self.point = point
        self.endpoint = max(point - roll, 0)
        self.roll = roll
        self.blot = blot

    def __eq__(self, other_move):
        if self.point == other_move.point and self.roll == other_move.roll:
            return True
        else:
            return False

    def __str__(self):
        start = "bar" if self.point == 25 else str(self.point)
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

    def count(self):
        counts = {}
        for move1 in self.moves:
            counts[str(move1)] = 0
            for move2 in self.moves:
                if move1 == move2:
                    counts[str(move1)] += 1
        return counts

    def __str__(self):
        moves_to_print = ""
        counts = self.count()
        if len(self.moves) == 0:
            moves_to_print = " (no play)"
        else:
            for move in counts:
                if counts[str(move)] > 1:
                    moves_to_print += " " + str(move) + "(" + str(counts[str(move)]) + ")"
                else:
                    moves_to_print += " " + str(move)
        return str(self.rolls[0]) + "-" + str(self.rolls[1]) + ":" + moves_to_print

    