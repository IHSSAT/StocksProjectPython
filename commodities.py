import Stocks
from googlefinance.client import get_price_data, get_prices_data, get_prices_time_data
import ta
class Commodity:
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
    def __init__(index, stockName, patternlength = 5, length = None, period=None):
        #create commodity parameter for google finance
        if period is not None and length is not None:
            self.param = Stocks.createParam(stock,index,length = length, period = period)
        elif period is not None and length is None:
            self.param = Stocks.createParam(stock,index,period = period)
        elif period is None and length is not None:
            self.param = Stocks.createParam(stock,index,length = length)
        else:
            self.param = Stocks.createParam(stock,index)
          
        self.stock = stockName
        self.index = index
        self.stockData = get_price_data(self.param)
        self.pattern = []
        self.volatility = findVolatility(self.stockData['Close'].tolist())

        
    
        
      

  
    
