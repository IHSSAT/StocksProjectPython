from iexfinance import get_historical_data
from datetime import datetime, timedelta
import json
import requests
from time import sleep
def makedatabasepatterns(name, findextremalength = 4, timelengthyears = 10): #makes json database of patterns and nexts
    a = open("Stats/" + name + ".json", 'w')
    end = datetime.now().date()
    start = datetime(end.year - 5, end.month, end.day)
    end = datetime(end.year, end.month, end.day)
    print(get_historical_data('AABA', start = start, end = end))

def downloadstockdata():
    nasd = open('NASD.txt')
    nyse = open('NYSE.txt')
    for stock in nasd:
        try:
            a = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=" + stock[:-1] + "&outputsize=full&apikey=2J8KPS27J02OVOSV")
            data = open('Stats/AllStockJson/' + stock[:-1] + ".json", 'w')
            json.dump(a.json(), data)
            data.close()
            print(stock[:-1])
            sleep(12.5)
        except:
            print(stock[:-1] + " is baaaaad")
            continue

    for stock in nyse:
        try:
            a = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=" + stock[:-1] + "&outputsize=full&apikey=2J8KPS27J02OVOSV")
            data = open('Stats/AllStockJson/' + stock[:-1] + ".json", 'w')
            json.dump(a.json(), data)
            data.close()
            print(stock[:-1])
            sleep(12.5)
        except:
            print(stock[:-1] + " is baaaaad")
            continue

downloadstockdata()
