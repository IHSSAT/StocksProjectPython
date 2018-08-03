import requests
import pandas as pd
from pandas.io.json import json_normalize
def makerequest(ticker, length):
    r = requests.get("https://api.iextrading.com/1.0/stock/" + ticker + "/chart/" + length).json()
    j = pd.DataFrame.from_dict(json_normalize(r), orient = "columns")
    return j
a = open("NASD.txt")
for line in a:
    print(line)
    makerequest(line[:-1].lower(), "1Y")


