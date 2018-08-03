from Lines import Point
from Lines import Line
import matplotlib.pyplot as plt
import pandas as pd
from tools import stddev
class Pattern:

    def __init__(self, pointsList, ratio = False):
        self.movelenth = len(pointsList) -1
        self.pointsList = pointsList
        a = []
        b = []
        for point in pointsList:
            a.append(point.x)
        self.timelength = max(a) - min(a)
        a.sort()
        for x in a:
            for point in pointsList:
                if x == point.x:
                    b.append(point.y)
        self.firstmove = (b[1] - b[0])/b[0]
        self.enddiff = (b[-1] - b[0]) / b[0]
        self.minimumdiff = (min(b) - b[0]) / b[0]
        self.maximumdiff = (max(b) - b[0]) / b[0]



        if ratio:
            rat = abs(self.firstmove)
            self.firstmove = self.firstmove/rat
            self.enddiff = self.enddiff/rat
            self.minimumdiff = self.minimumdiff/rat
            self.maximumdiff = self.maximumdiff/rat

        self.moves = []
        x = 0
        while x < len(pointsList) - 1:
            self.moves.append((a[x+1] - a[x], (100 * (b[x + 1] - b[x]))/b[x])) #adds tuple of (movelenth, percent move)
            x = x+1
        self.ratiomoves = []
        x = 0
        while x < len(self.moves):
            self.ratiomoves.append(((self.moves[x][0]/self.moves[0][0]), (self.moves[x][1]/abs(self.moves[0][1])))) #reports each move in relationship to the first move
            x = x+1
        self.type = "None"
    def plotPattern(self, ratio = True, plot = False):
        lines = []
        if ratio:
            position = [0,0]
            for move in self.ratiomoves:
                x = Line()
                x.pointSlope(Point(position[0], position[1]), move[1] / move[0])
                x.startLoc = position[0]
                x.endLoc = move[0] + x.startLoc
                lines.append(x)
                position[0] = x.endLoc
                position[1] = position[1] + move[1]
            for line in lines:
                line.plotLine()
        else:
            position = [0,0]
            for move in self.moves:
                x = Line()
                x.pointSlope(Point(position[0], position[1]), move[1] / move[0])
                x.startLoc = position[0]
                x.endLoc = move[0] + x.startLoc
                lines.append(x)
                position[0] = x.endLoc
                position[1] = position[1] + move[1]
            for line in lines:
                line.plotLine()
        if plot:
            plt.show()
    def convertpdSeries(pdSeriesExtrema): #Converts pd series to a list of points
        locations = list(pdSeriesExtrema.index.values)
        prices = pd.Series.tolist(pdSeriesExtrema)
        z = 0
        points = []
        while z < len(locations):
            a = Point(locations[z], prices[z])
            points.append(a)
            z = z + 1
        return points

    def comparePattern(self, pattern, ratio = True):
        if ratio:
            a = self.ratiomoves
            b = pattern.ratiomoves
        else:
            a = self.moves
            b = pattern.moves
        x = 0
        while x < len(a):
            if (a[x][0])/(b[x][0]) > 1.2 or (a[x][0])/(b[x][0]) < 0.8:
                return False
            if (a[x][1])/(b[x][1]) > 1.2 or (a[x][1])/(b[x][1]) < 0.8:
                return False
            x = x+1
        return True




