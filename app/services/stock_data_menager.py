from db.crud import upsert_raw_data
from db.models import RawStockData,StockData
class StockDataMengaer():
    """
    Service layer responsible for orchestrating stock data retrieval and processing.
    Data are requested through this class.
    Data are first read from the database.
    If the data does not exist in the database, the external API is called,
    and the ETL process is executed.
    """
    def __init__(self,raw_data:RawStockData,stockdata:StockData,):
        pass