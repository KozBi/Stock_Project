from app.db.CRUD.stock_crud import upsert_stock_data, insert_non_trading_days
from app.services.stock_calendar import any_missing_dates

def write_stock_data_DB(data:dict):

#1 create list of all days
    list_of_days=[]
    for day in data['date']:
        list_of_days.append(day)

#2 call a function to find a missing days
    days_without_trade=any_missing_dates(list_of_days)
    
    if days_without_trade:
        insert_non_trading_days(days_without_trade)

#3 inster data to DB from API
    upsert_stock_data(data)
        
