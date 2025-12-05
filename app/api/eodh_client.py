from eodhd import APIClient
from dotenv import load_dotenv


load_dotenv()

# api = APIClient("demo")

# symbol='AAPL.US'
# resp = api.get_eod_historical_stock_market_data(symbol = symbol, period='d', from_date = '2023-01-01', to_date = '2023-01-15', order='a')
# print(resp)

# print(resp[1]['date'], symbol)

class EODH_Client():
    def __init__(self,user='demo'):

        self.api = APIClient(user)

    def get_historical_data(self, _symbol,_period,_from_date:str,_to_date:str,_order='a'):
        """
        Fetch historical stock data from EODHD API.

        Args:
            symbol (str): Stock symbol, e.g., "AAPL.US"
            period (str): Data period, e.g., 'd' for daily
            from_date (str): Start date in 'YYYY-MM-DD'
            to_date (str): End date in 'YYYY-MM-DD'
            order (str): Sorting order, 'a' = ascending, 'd' = descending

        Returns:
            list: List of stock data dictionaries, or None if an error occurs
        """
        try:
            response=self.api.get_eod_historical_stock_market_data(symbol = _symbol,
                                                    period=_period, 
                                                    from_date =_from_date,
                                                    to_date = _to_date,
                                                    order=_order)
            return response
        except Exception as e:
            print(f"Error fetching data for {_symbol}: {e}")
            return None