from eodhd import APIClient
from dotenv import load_dotenv
import pandas as pd


load_dotenv()

api = APIClient("demo")

symbol='AAPL.US'
resp = api.get_eod_historical_stock_market_data(symbol = symbol, period='d', from_date = '2023-01-01', to_date = '2023-01-15', order='a')
print(resp)

print(resp[1]['date'], symbol)