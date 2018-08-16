from iexfinance import get_historical_data
from datetime import datetime, timedelta
import json
import Stocks
from Patterns import Pattern
import requests
from time import sleep
def makedatabasepatterns(name, findextremalength = 4): #makes json database of patterns and nexts
    a = open("Stats/" + name + ".json", 'w')


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


def combinejson():
    import os
    directory = os.fsencode('C:/Users/Patrick Yuan/Desktop/AllStockJson')
    listofstocks = list()
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        listofstocks.append(filename)
    finaldata = dict()
    for stock in listofstocks:
        with open("C:/Users/Patrick Yuan/Desktop/AllStockJson/" + stock) as a:
            data = json.load(a)
        stockname = stock.strip('.json')
        finaldata[stockname] = data
    with open('Stats/AllStockJson/FINALDATACOMPLETEJSON.json', 'w') as a:
        print('dumping')
        json.dump(finaldata, a)

def findavgvolatility():
    a = open("Stats/volatilitynew.txt")
    count = 0
    total = 0
    for line in a:
        colon = line.find(':')
        number = float(line[colon + 2: -1])
        total = total + number
        count = count + 1
    print(total/count)

def removebadstocks():
    a = open('Stats/volatility.txt')
    e = open('shittystocks.txt', 'w')
    lines = []
    for line in a:
        colon = line.find(':')
        b = requests.get('https://api.iextrading.com/1.0/stock/' + line[:colon] + '/stats')
        c = requests.get('https://api.iextrading.com/1.0/stock/' + line[:colon] + '/quote')
        volume = c.json()
        stock = b.json()
        if int(stock['marketcap']) == 0 and int(volume['avgTotalVolume']) > 5000:
            lines.append(line)
        else:
            if int(stock['marketcap']) > 40000000 and int(volume['avgTotalVolume']) > 5000:
                lines.append(line)
            else:
                if (int(stock['marketcap']) > 100000000 or int(volume['avgTotalVolume']) > 50000) and (int(stock['marketcap']) > 5000000 and int(volume['avgTotalVolume']) > 1000): lines.append(line)
                else:
                    print(line[:colon] + ' ' + str(stock['marketcap']) + " " + str(volume['avgTotalVolume']))
                    e.write(line[:colon] + '\n')
                    e.flush()
    d = open('Stats/volatilitynew.txt', 'w')
    for line in lines:
        d.write(line)


combinejson()