
from iexfinance import get_historical_data
from datetime import datetime




import Stocks


def yolo():
    end = datetime.now()
    end = end.replace(hour = 0, minute =0, second = 0, microsecond = 0)
    start = datetime(end.year, end.month, end.day-1)
    w = open('NASD.txt')
    for line in w:
        df = get_historical_data(line[:len(line)-1], start=start, end=end, output_format='pandas')
        print(line[:-1])
yolo()