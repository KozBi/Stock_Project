from eodhd import APIClient
import pandas as pd


api = APIClient("demo")

resp = api.get_eod_historical_stock_market_data(symbol = 'AAPL.US', period='d', from_date = '2023-01-01', to_date = '2023-01-15', order='a')
print(resp)