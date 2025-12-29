from app.db.CRUD.stock_crud import upsert_raw_data , data_ticker_valid
from services.write_stock_data_DB import write_stock_data_DB
from db.models import RawStockData,StockData
from app.api.eodh_client import EODH_Client
from datetime import datetime


import logging


class StockDataMengaer():
    """
    Service layer responsible for orchestrating stock data retrieval and processing.
    Data are requested through this class.
    Data are first read from the database.
    If the data does not exist in the database, the external API is called,
    and the ETL process is executed.
    """
    def __init__(self,raw_data:RawStockData,session:StockData,eodh_client:EODH_Client):
        self.raw_data_db=raw_data
        self.session=session
        self.eodh_client=eodh_client

    def get_stock_data(ticker:str, from_date:datetime=datetime.now(), to_date:datetime=datetime.now()):
        """Check DB data if data is not found, then call api method."""
        print(to_date)
    

    def _check_data(self,ticker:str, from_date:datetime, to_date:datetime):
        """Check if data is available"""
        result=data_ticker_valid(self.session,ticker,from_date,to_date)
        return result
    
    def _write_data(self,ticker:str, from_date:datetime, to_date:datetime):
        """Write date to DB"""
        write_stock_data_DB()
