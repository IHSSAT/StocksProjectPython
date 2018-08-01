import math
from typing import List

import matplotlib.pyplot as plt
import numpy as np

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
        self.lineType = ["None"]
        self.startLoc = None
        self.endLoc = None
        self.time = None
        self.bouncePt = [] #List of points that bounce off trendline
        self.overPoints = [] #List of points that bounce or go under/over trendline.
        self.significance = None #Make calculations to assign rating of significance to each trendline.

        if len(self.bouncePt) == 0 or len(self.overPoints) ==0 :
            self.bouncePct = None
        else:
            self.bouncePct = len(self.bouncePt)/len(self.overPoints)
            
        if self.startLoc == None or self.endLoc == None:
            self.timeDist = None
        else: 
            self.timeDist = self.endLoc - self.startLoc
            

        
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
    def plotLine(self, length = 0, show = False):
        if length != 0:
            plt.plot([0,length], [self.findY(0), self.findY(length)])
        elif self.startLoc is not None and self.endLoc is not None:
            plt.plot([self.startLoc, self.endLoc], [self.findY(self.startLoc), self.findY(self.endLoc)])
        else:
            plt.plot([0,300],[self.findY(0), self.findY(300)])
        if show:
            plt.show()


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
        pct = ((y - y1) / (y1))
        dst = y - y1
        if arithmetic == False:
            return pct
        elif arithmetic == True:
            return dst
        else:
            return None
        # Guidance: 2 - 3 percent seems acceptable

    def twoLineAngle(self, line2): #may not do what is supposed to, change later
        try:
            m1 = self.slope
            m2 = line2.slope
            ans = math.degrees(math.atan((m1 - m2)/(1 + m1*m2)))
            if ans>0:
                return ans
            else:
                return ans+180
        except:
            return 90
    def combineLines(self, line):
        a = (self.slope + line.slope)/2
        b = (self.yint + line.yint)/2
        self.slope = a
        self.yint = b