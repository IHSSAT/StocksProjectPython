from Lines import Line
from Lines import Point
from googlefinance.client import get_price_data, get_prices_data, get_prices_time_data
import Stocks
import time
import math

def makeTrendLines(locations, prices):
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
            line1.endLoc = points[idx+1].x
            trendLines.append(line1)
            idx = idx + 1
    return trendLines


def trendLineIntersect(line, completeStockData, threshhold = 0.025, time = 10): #returns True if Trendline does NOT intersect with graph
    loc = line.startLoc
    above = 0
    below = 0
    for stock in completeStockData[loc:]:
        if stock > line.findY(completeStockData.index(stock)): #y value of line at the x value of the stock
            above = above + 1
        elif stock < line.findY(completeStockData.index(stock)):
            below = below + 1
    if (above / (above + below)) >= 0.5:
        for stock in completeStockData[loc:len(completeStockData)-time-1]:
            if stock < (1-threshhold)*line.findY(completeStockData.index(stock)):
                return False
        line.lineType = 'support'
        line.time = time
        return True
    elif (above / (above + below)) < 0.5:
        for stock in completeStockData[loc:len(completeStockData)-time-1]:
            if stock > (1+threshhold)*line.findY(completeStockData.index(stock)):
                return False
        line.lineType = 'resistance'
        line.time = time
        return True
    else:
        return "no data"

def signal(line, completeStockData, angle, time1 = None, threshhold = 0.025):
    if time1 is None and line.time is None:
        time = 10
    elif time1 is not None:
        time = int(time1)
    else:
        time = line.time

    if len(completeStockData)>= time:
        data = completeStockData[len(completeStockData)-time:]
    else:
        data = completeStockData
    # if stock crosses over trendline and exceeds threshhold, set variable "crossover" to True. Else, false.
    crossover = False
    if line.lineType == 'support':
        minimum = min(data)
        location = completeStockData.index(minimum)
        if minimum < (1 - threshhold)*line.findY(location):
            crossover = True
    elif line.lineType == 'resistance':
        maximum = max(data)
        location = completeStockData.index(maximum)
        if maximum > (1 + threshhold) * line.findY(location):
            crossover = True
    else:
        crossover = "lineTypes are not set; please set thanks or they are messed up pls fix"
    return crossover #add in angle feature later

    # Calculate angle; should investigate angle dynamics and average angles first. Do a statistical scan of the market.
    """
    total = 0
    for stock in data:
        total = total + stock
    slope = total/time
    point = Point(math.floor(time/2),data[math.floor(time/2)])
    stockLine = Line()
    stockLine.pointSlope(point, slope)"""


def removeLinesInt(trendLines, completeStockData, threshhold = 0.025): #takes trendlines and removes those that intersect w/ graph
    total = []
    for line in trendLines:
        if Stocks.trendLineIntersect(line, completeStockData, threshhold):
            total.append(line)
    return total

def listinList(list1,inList2):
    x=0
    for element in list1:
        if element in inList2:
            x = x+1
            inList2.remove(element)
    if x==len(list1):
        return True
    else:
        return False

def filterLines(locations, prices, trendLines, dist = 2.5):
    if len(locations) != len(prices):
        return "wrong"
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
                trendLine.bouncePoints.append(point)
                trendLine.endLoc = point.x
        endLoc = trendLine.endLoc
        endIdx = locations.index(endLoc)
        for point in points[startIdx:(endIdx+1)]:
            trendLine.overPoints.append(point)
        # label line (line type)
    # remove "duplicate" lines
    z = 0
    while z<len(trendLines)-1:
        x = trendLines[z].bouncePoints
        for trendline in trendLines[z+1:]:
            if Stocks.listinList(x, trendline.bouncePoints):
                trendLines.remove(trendLines[z])

            
def findExtrema(length, data):
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
    for price in data:
        idx = data.index(price)
        if idx < (len(data) - length):
            a = 0
            b = 0
            for num in numList:
                if data[idx] >= data[idx + num]:
                    a = a + 1
                if data[idx] <= data[idx + num]:
                    b = b + 1
            if a == len(numList):
                locationmax.append(idx)
                pricemax.append(price)
            if b == len(numList):
                locationmin.append(idx)
                pricemin.append(price)
        else:
            continue
    return [locationmax, pricemax, locationmin, pricemin]


def createParam(stock, index, length="86400", period="1Y"):
    param = {
        'q': str(stock),
        'i': str(length),
        'x': str(index),
        'p': str(period)
    }
    return param


def scan(indexFile, index):
    lst1 = list()
    idx = open(indexFile)
    for line in idx:
        lst1.append(line)
    xx = 0
    while xx < len(lst1):
        a = lst1[xx]
        param1 = Stocks.createParam(a[:len(a) - 1], index)
        try:
            data = get_price_data(param1)
            dsclose = data['Close'].tolist()
            # Do processing here
            #
            #
            #
            #
            xx = xx + 1
        except:
            print('sleeping two minutes...')
            time.sleep(120)

