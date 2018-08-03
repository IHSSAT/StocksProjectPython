from iexfinance import get_historical_data
from datetime import datetime
start = datetime(2018, 7, 2)
end = datetime(2018, 8, 2)
df = get_historical_data("AVLRRRRRRR", start=start, end=end, output_format='pandas')
print(df)
