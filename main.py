from iexfinance import get_historical_data
from datetime import datetime
import Stocks
import time
import threading
def stupid():
    start = datetime(2017, 5, 24)
    end = datetime(2018, 5, 24)
    e = open("NYSE.txt")
    d = open("NASD.txt")
    b = open("shittystocks.txt",'w')
    c = open("volatility.txt", "w")
    a = []
    for stock in e:
        a.append(stock)
    for stock in d:
        a.append(stock)
    for stock in a:
        try:
            df = get_historical_data(stock[:-1], start=start, end=end, output_format='pandas')
        except:
            b.write(stock)
            b.flush()
            print(stock[:-1] + "wroooooong")
            continue
        if len(df['close']) < 3:
            continue
        c.write(stock[:-1] + ": " + str(Stocks.findVolatility(df['close'])) + "\n")
        c.flush()
        print(stock[:-1])
stupid()