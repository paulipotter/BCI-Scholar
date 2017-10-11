from math import sqrt


class Point(object):
    '''Creates a point on a coordinate plane with values x and y.'''

    def __init__(self, calftag, x, y):
        '''Defines x and y variables'''
        self.X = x
        self.Y = y
        self.calftag = calftag

    def __str__(self):
        return "Point(%s,%s)" % (self.X, self.Y)

    def getX(self):
        return self.X

    def getY(self):
        return self.Y

    def distance(self, other):
        dx = self.X - other.X
        dy = self.Y - other.Y
        return sqrt(dx ** 2 + dy ** 2)
