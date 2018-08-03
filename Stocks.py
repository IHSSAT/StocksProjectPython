from Lines import Line
from Lines import Point
import Stocks
import time
import pandas as pd
import math

#ADD IN HORIZONTAL SUPPORTS AND RESISTANCE! 
#ADD IN VOLATILITY ADJUSTMENTS!!
def numDiff(a,b):
    return ((b/a)-1)*100
def findVolatility(pdSeries):
    series = pdSeries.tolist()
    x = 0
    final = 0
    while x < len(series)-1:
        final = final + abs(numDiff(series[x],series[x+1]))
        x = x+1
    return final/x
def makeTrendLines(pdSeries):
    locations = list(pdSeries.index.values)
    prices = pd.Series.tolist(pdSeries)
    if len(locations) != len(prices):
        return "wrong"
    z = 0
    trendLines = []
    points = []
    while z < len(locations):
        a = Point(locations[z], prices[z])
        points.append(a)
        z = z + 1
    for point in points:
        idx = points.index(point)
        while idx < (len(points) - 1):
            line1 = Line()
            line1.twoPoint(point, points[idx + 1])
            line1.startLoc = point.x
            line1.endLoc = points[idx + 1].x
            trendLines.append(line1)
            idx = idx + 1
    return trendLines


def trendLineIntersect(line, pdSeries, threshold=0.025, time=10, vola = False):  # returns True if Trendline does NOT intersect with graph beyond threshold
    completeStockData = pdSeries.tolist()
    if vola is False:
        volatility = findVolatility(pdSeries)
    else:
        volatility = vola
    loc = line.startLoc
    above = 0
    below = 0
    if loc<len(completeStockData) - time - 1 - 1:
        for stock in completeStockData[loc:len(completeStockData) - time - 1]:
            if stock > line.findY(completeStockData.index(stock)):  # y value of line at the x value of the stock
                above = above + 1
            elif stock < line.findY(completeStockData.index(stock)):
                below = below + 1
        if (above / (above + below)) >= 0.5:
            for stock in completeStockData[loc:len(completeStockData) - time - 1]:
                if stock < (1 - threshold) * line.findY(completeStockData.index(stock)):
                    return False
            line.lineType[0] = 'support'  # sets linetype
            line.time = time  # sets amount of time before present day that line was tested for intersection with stock graph
            return True
        elif (above / (above + below)) < 0.5:
            for stock in completeStockData[loc:len(completeStockData) - time - 1]:
                if stock > (1 + threshold) * line.findY(completeStockData.index(stock)):
                    return False
            line.lineType[0] = 'resistance'
            line.time = time
            return True
        else:
            return "no data"
    else:
        return False

def signal(line, pdSeries, angle, time1=None, threshold=0.025, vola = False):
    completeStockData = pdSeries.tolist()
    if vola is False:
        volatility = findVolatility(pdSeries)
    else:
        volatility = vola
    if time1 is None and line.time is None:
        time = 10
    elif time1 is not None:
        time = int(time1)
    else:
        time = line.time

    if len(completeStockData) >= time:
        data = completeStockData[len(completeStockData) - time:]
    else:
        data = completeStockData
    # if stock crosses over trendline and exceeds threshold, set variable "crossover" to True. Else, false.
    crossover = False
    if line.lineType[0] == 'support':
        minimum = min(data)
        location = completeStockData.index(minimum)
        if minimum < (1 - threshold) * line.findY(location):
            crossover = True
    elif line.lineType[0] == 'resistance':
        maximum = max(data)
        location = completeStockData.index(maximum)
        if maximum > (1 + threshold) * line.findY(location):
            crossover = True
    else:
        crossover = "lineTypes are not set; please set thanks or they are messed up pls fix"
    return crossover

    # add in angle feature later

    # Calculate angle; should investigate angle dynamics and average angles first. Do a statistical scan of the market.
    """
    total = 0
    for stock in data:
        total = total + stock
    slope = total/time
    point = Point(math.floor(time/2),data[math.floor(time/2)])
    stockLine = Line()
    stockLine.pointSlope(point, slope)"""


def removeLinesInt(trendLines, pdSeries, threshold=0.025):  # takes trendlines and removes those that intersect w/ graph
    total = []
    for line in trendLines:
        if Stocks.trendLineIntersect(line, pdSeries, threshold):
            total.append(line)
    return total


def listinList(a, b):
    if set(a).issubset(b):
        return True
    else:
        return False

def similarSlope(slope1, slope2, threshold = 0.05):
    diff = abs((slope1-slope2)/slope1)
    diff1 = abs((slope1-slope2)/slope2)
    if diff<threshold or diff1<threshold:
        return True
    else:
        return False

def filterLines(pdSeries, pdSeriesExtrema, trendLines, dist=0.025, vola = False):
    locations = list(pdSeriesExtrema.index.values)
    if vola is False:
        volatility = findVolatility(pdSeries)
    else:
        volatility = vola
    #print(volatility)
    prices = pd.Series.tolist(pdSeriesExtrema)
    z = 0
    points = []
    while z < len(locations):
        a = Point(locations[z], prices[z])
        points.append(a)
        z = z + 1
    for trendLine in trendLines:
        startLoc = trendLine.startLoc
        startIdx = locations.index(startLoc)
        for point in points[startIdx:]:
            distance = trendLine.linePointDist(point)
            if abs(distance) < dist:
                trendLine.bouncePt.append(point)
                trendLine.endLoc = point.x
        #print(len(trendLine.bouncePt))
        endLoc = trendLine.endLoc
        endIdx = locations.index(endLoc)
        for point in points[startIdx:(endIdx + 1)]:
            trendLine.overPoints.append(point)
    # remove "duplicate" lines
    z = 0
    while z < len(trendLines) - 1:
        for trendline in trendLines:
            if listinList(trendline.bouncePt, trendLines[z].bouncePt) and similarSlope(trendLines[z].slope, trendline.slope, 0.5):
                if len(trendline.bouncePt) > len(trendLines[z].bouncePt):
                    trendLines.remove(trendLines[z])
                if len(trendline.bouncePt) < len(trendLines[z].bouncePt):
                    trendLines.remove(trendline)
                if len(trendline.bouncePt) == len(trendLines[z].bouncePt):
                    trendline.combineLines(trendLines[z])
                    trendLines.remove(trendLines[z])
        z = z+1
    for trendline in trendLines:
        values = []
        for point in trendline.bouncePt:
            values.append(point.x)
        if abs(numDiff(max(values), min(values))) < 0.05:
            trendline.slope = 0
            avg = 0
            for element in trendline.bouncePt:
                avg = avg + element.x
            trendline.yint = avg/len(values)
            trendline.lineType.append("horiz")
    return trendLines


def findExtrema(length, pdSeries, type):
    data = pdSeries.tolist()
    index = list(range(len(data)))
    ## actually works!
    x = 1
    numList = []
    locationmax = []
    pricemax = []
    locationmin = []
    pricemin = []
    while x <= length:
        numList.append(x)
        numList.append(-1 * x)
        x = x + 1
    for idx in index:
        if idx < (len(data) - length):
            a = 0
            b = 0
            for num in numList:
                if data[idx] > data[idx + num]:
                    a = a + 1
                if data[idx] < data[idx + num]:
                    b = b + 1
            if a == len(numList):
                locationmax.append(idx)
                pricemax.append(data[idx])
            if b == len(numList):
                locationmin.append(idx)
                pricemin.append(data[idx])
        else:
            continue
    one = pd.Series(pricemax, locationmax, name="max")
    two = pd.Series(pricemin, locationmin, name="min")
    if type == "max":
        return one
    elif type == "min":
        return two
    elif type == "all":
        return one.combine_first(two)
    else:
        return "type not set"


# def createParam(stock, index, length="86400", period="1Y"): #Useless right now, switched clients
#     param = {
#         'q': str(stock),
#         'i': str(length),
#         'x': str(index),
#         'p': str(period)
#     }
#     return param


# def scan(indexFile, index):
#     lst1 = list()
#     idx = open(indexFile)
#     for line in idx:
#         lst1.append(line)
#     xx = 0
#     while xx < len(lst1):
#         a = lst1[xx]
#         param1 = Stocks.createParam(a[:len(a) - 1], index)
#         try:
#             data = get_price_data(param1)
#             dsclose = data['Close'].tolist()
#             # Do processing here
#             #
#             #
#             #
#             #
#             xx = xx + 1
#         except:
#             print('sleeping two minutes...')
#             time.sleep(120)
#
#
def horizLines(pdSeries, length = 10, type = "max", threshold=0.025, time=10): #FIX
    trendlines = []
    pdSeriesExtrema = findExtrema(length, pdSeries, type)
    locations = list(pdSeriesExtrema.index.values)
    prices = pd.Series.tolist(pdSeriesExtrema)
    z = 0
    points = []
    while z < len(locations):
        a = Point(locations[z], prices[z])
        points.append(a)
        z = z + 1
    for point in points:
        x = Line(0, point.y)
        if trendLineIntersect(x, pdSeries, threshold, time):
            x.lineType.append("horiz")
            x.bouncePt.append(point)
            x.overPoints.append(point)
            trendlines.append(x)

