from app.db.CRUD.stock_crud import upsert_stock_data, insert_non_trading_days
from app.services.stock_calendar import any_missing_dates
from datetime import date,datetime
from logging import logger


class ValidationError(Exception):
    """Raised when stock data validation fails."""
    pass

def _validate_data(data: dict) -> None:
    """Validate input stock data."""
    if not data:
        raise ValidationError("Data dictionary is empty")

    if 'date' not in data or not data['date']:
        raise ValidationError("Missing or empty 'date' field")
    
    if not isinstance(data.get('date'), date):
        raise ValidationError("'date' must be datetime.date")
    
def insert_non_trading_days():
    pass
    #     data:dict,
    #     missing_dates: list[datetime]
    # ):
    #     """
    #     Fill missing dates with deafult values, 
    #     trade days - FALSE
    #     """
    #     for d in missing_dates:
    #         stmt = insert(StockData).values(
    #             ticker=ticker,
    #             stock_date=d,
    #             trade_day=False,
    #             Open=0,
    #             high=0,
    #             low=0,
    #             close=0,
    #             adjusted_close=0,
    #             volume=0
    #         ).on_conflict_do_nothing(
    #             index_elements=["ticker", "stock_date"]
    #         )
    #         db.execute(stmt)
    #     db.commit()
        

def write_stock_data_DB(data:dict,database) -> bool:
    """
    Write data to the Database
    :param data: Dictionary containing stock prices, days and volumes
    return True if data has been written sucessfully
    """
#1 validate data
    try:
        _validate_data(data)
    except ValidationError as e:
        logger.info(f"Skipped record: {e}")
        return False

#2 create list of all days
    list_of_days=[]
    for day in data['date']:
        list_of_days.append(day)

#3 call a function to find a missing days
    days_without_trade=any_missing_dates(list_of_days)
    
#4 update data with days without trade if any exist
    if days_without_trade:
        insert_non_trading_days(days_without_trade)

#5 inster data to DB from API
    upsert_stock_data(data)
    return True
        
