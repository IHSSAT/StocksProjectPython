from Lines import Line
from Lines import Point
from googlefinance.client import get_price_data, get_prices_data, get_prices_time_data
import Stocks
import time

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
            line1.twoPoint(point, poin
            idx = idx + 1
    return trendLines

ts[idx + 1])
            line1.startLoc = point.x
            line1.endLoc = points[idx+1].x
            trendLines.append(line1)
def trendLineIntersect(line, completeStockData, threshhold = 0.975):
    loc = line.startLoc
    above = 0
    below = 0
    for stock in completeStockData[loc:]:
        if stock > line.findY(completeStockData.index(stock)):
            above = above + 1
        elif stock < line.findY(completeStockData.index(stock)):
            below = below + 1
    if (above / (above + below)) >= threshhold or (below / (above + below)) >= threshhold:
        return True
    else:
        return False


def filterTrendLines(trendLines, completeStockData, threshhold = 0.975):
    final = []
    for trendLine in trendLines:
        loc = trendLine.startLoc
        above = 0
        below = 0
        for stock in completeStockData[loc:]:
            if stock > trendLine.findY(completeStockData.index(stock)):
                above = above + 1
            elif stock < trendLine.findY(completeStockData.index(stock)):
                below = below + 1
        if (above / (above + below)) >= threshhold or (below / (above + below)) >= threshhold:
            final.append(trendLine)
    return final


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
            xx = xx + 1
        except:
            print('sleeping two minutes...')
            time.sleep(120)

