from app.db.CRUD.stock_crud import upsert_stock_data, insert_non_trading_days
from app.services.stock_calendar import any_missing_dates
from datetime import date
from logging import Logger
class ValidationError(Exception):
    pass

def _validate_data(data: dict) -> None:
    """Validate input stock data."""
    if not data:
        raise ValueError("Data dictionary is empty")

    if 'date' not in data or not data['date']:
        raise ValueError("Missing or empty 'date' field")
    
    if not isinstance(data.get('date'), date):
        raise TypeError("'date' must be datetime.date")
        

def write_stock_data_DB(data:dict,database) -> None:
    """
    Write data to the Database
    :param data: Dictionary containing stock prices, days and volumes
    """
#1 validate date
    try:
        _validate_data(data)
    except ValidationError as e:
        logger.info(f"Skipped record: {e}")

#2 create list of all days
    list_of_days=[]
    for day in data['date']:
        list_of_days.append(day)

#3 call a function to find a missing days
    days_without_trade=any_missing_dates(list_of_days)
    
    if days_without_trade:
        insert_non_trading_days(days_without_trade)

#4 inster data to DB from API
    upsert_stock_data(data)
        
