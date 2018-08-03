from iexfinance import get_historical_data
from datetime import datetime
import Stocks
import time
start = datetime(2017, 5, 24)
end = datetime(2018, 5, 24)
a = open("NYSE.txt")
d = open("NASD.txt")
b = open("shittystocks.txt",'w')
c = open("volatility.txt", "w")
for stock in a:
    try:
        df = get_historical_data(stock[:-1], start=start, end=end, output_format='pandas')
        c.write(str(Stocks.findVolatility(df['close'])) + "\n")
    except:
        b.write(stock)
        continue
