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


from app.api.eodh_client import EODH_Client

@pytest.fixture
def clinet():
    eodh=EODH_Client()
    return eodh


def test_tet_historical_data(clinet,capsys):
  #  clinet:EODH_Clients
    symbol='AMZN.US'
    from_date='2025-12-01'
    to_date='2025-12-05'
    result=clinet.get_historical_data(symbol,from_date,to_date)

    assert len(result)==5
    with capsys.disabled():
        print('XXXXXXXXXXXXXXXXX')
        print(result)
        for x in result:
            print(x)
            print('\n')

