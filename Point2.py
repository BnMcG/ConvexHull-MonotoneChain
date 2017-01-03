class Point2:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point<" + str(self.x) + "," + str(self.y) + ">"