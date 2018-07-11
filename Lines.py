import math


class Point:
    def __init__(self, a=None, b=None):
        self.x = a
        self.y = b

    def printPoint(self):
        print("(" + str(self.x) + "," + str(self.y) + ")")


class Line(Point):
    def __init__(self, mslope=1, yintercept=0):
        self.slope = mslope
        self.yint = yintercept
        self.lineType = None
        self.startLoc = None
        self.endLoc = None

    def slopeInt(self, mslope, yintercept):
        self.slope = mslope
        self.yint = yintercept

    def pointSlope(self, point, slope):
        self.slope = slope
        self.yint = point.y - slope * point.x

    def twoPoint(self, point1, point2):
        slp = (point1.y - point2.y) / (point1.x - point2.x)
        self.slope = slp
        self.yint = point1.y - slp * point1.x

    def findY(self, x):
        return (self.slope) * x + self.yint

    def findX(self, y):
        return (y - self.yint) / self.slope

    def linesIntersect(self, line):
        if self.slope == line.slope and self.yint != line.yint:
            return "lines are paralell"
        elif self.slope == line.slope and self.yint == line.yint:
            return "lines are the same"
        else:
            x = (line.yint - self.yint) / (self.slope - line.slope)
            y = self.findY(x)
            return Point(x, y)

    def printLine(self):
        a = str(self.slope)
        b = str(self.yint)
        print("y = " + a + "x + " + b)

    def twoPointDist(point1, point2):
        x2 = point2.x
        x1 = point1.x
        y2 = point2.y
        y1 = point1.y
        return math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))

    def linePointDist(self, point, arithmetic=False):
        x = point.x
        y = point.y
        y1 = self.findY(x)
        pct = ((y - y1) / (y1)) * 100
        dst = y - y1
        if arithmetic == False:
            return pct
        elif arithmetic == True:
            return dst
        else:
            return None
        # Guidance: 2 - 3 percent seems acceptable
