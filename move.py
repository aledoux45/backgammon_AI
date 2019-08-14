"""
Describes a backgammon move
"""


class Move:
    def __init__(self, point, roll, blot=False):
        self.startpoint = point
        self.endpoint = max(point - roll, 0)
        self.roll = roll

    def __str__(self):
        if self.blot:
            return str(self.startpoint) + "/" + str(self.endpoint) + "*"
        else:
            return str(self.startpoint) + "/" + str(self.endpoint)