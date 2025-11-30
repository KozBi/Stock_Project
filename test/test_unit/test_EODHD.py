import pytest

from eodhd import APIClient
from dotenv import load_dotenv


def test_api_connection():

    load_dotenv()
    api = APIClient("demo")

    symbol='AAPL.US'
    resp = api.get_eod_historical_stock_market_data(symbol = symbol, period='d', from_date = '2023-01-01', to_date = '2023-01-15', order='a')
    print(resp)

    assert f"{resp[1]['date']}, {symbol}" =="2023-01-04, AAPL.US" , resp
   # assert 1==2, resp

