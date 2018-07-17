from googlefinance.client import get_price_data, get_prices_data, get_prices_time_data
import matplotlib.pyplot as plt
from pprint import pprint
from Lines import Line
import Stocks
param = {
    'q': "AAPL",  # Stock symbol (ex: "AAPL")
    'i': "86400",  # Interval size in seconds ("86400" = 1 day intervals)
    'x': "NASD",  # Stock exchange symbol on which stock is traded (ex: "NASD")
    'p': "1Y"  # Period (Ex: "1Y" = 1 year)
}
data = get_price_data(param)
dsclose = data['Close'].tolist()
dsopen = data['Open'].tolist()
dshigh = data['High'].tolist()
dslow = data['Low'].tolist()
dsvolume = data['Volume'].tolist()
#print(data)

x = Stocks.findExtrema(4, data['Close'], "min")
trendlines = Stocks.makeTrendLines(x)
filteredlines = Stocks.removeLinesInt(trendlines, data['Close'], threshold=0.015)
morefiltered = Stocks.filterLines(x,filteredlines, dist = 0.01)

y = Stocks.findExtrema(4, data['Close'], "max")
trendlines1 = Stocks.makeTrendLines(y)
filteredlines1 = Stocks.removeLinesInt(trendlines1, data['Close'], threshold=0.015)
morefiltered1 = Stocks.filterLines(y,filteredlines1, dist = 0.01)



#print(len(morefiltered))
plt.plot(dsclose)
plt.scatter(list(x.index.values),x.tolist())

for line in morefiltered:
    line.plotLine()
for line in morefiltered1:
    line.plotLine()
plt.show()
