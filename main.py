from googlefinance.client import get_price_data, get_prices_data, get_prices_time_data
import matplotlib.pyplot as plt
from pprint import pprint
from Lines import Line
import Stocks
param = {
    'q': "A",  # Stock symbol (ex: "AAPL")
    'i': "86400",  # Interval size in seconds ("86400" = 1 day intervals)
    'x': "NYSE",  # Stock exchange symbol on which stock is traded (ex: "NASD")
    'p': "1M"  # Period (Ex: "1Y" = 1 year)
}
data = get_price_data(param)
dsclose = data['Close'].tolist()
dsopen = data['Open'].tolist()
dshigh = data['High'].tolist()
dslow = data['Low'].tolist()
dsvolume = data['Volume'].tolist()
#print(data)

line1 = Line(0, 3)
line2 = Line(1, -2)
print(Line.twoLineAngle(line1, line2))