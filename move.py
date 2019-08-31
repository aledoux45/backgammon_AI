"""
Describes a backgammon move
"""


class Move:
    def __init__(self, point, roll, blot=False):
        self.startpoint = point
        self.endpoint = max(point - roll, 0)
        self.roll = roll
        self.blot = blot

    def __str__(self):
        start = "bar" if self.startpoint == 25 else str(self.startpoint)
        finish = "off" if self.endpoint == 0 else str(self.endpoint)
        blot = "*" if self.blot else ""
        return start + "/" + finish + blot