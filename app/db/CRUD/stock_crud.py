from sqlalchemy.orm import Session
from ..models import RawStockData, StockData
from datetime import date
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import update, select
from datetime import datetime
from datetime import timedelta
import logging


def upsert_stock_data(db: Session, ticker: str, stock_data: dict[str],trade_day=True):
    """
    Upsert stock data, 
    trade days - deafult True
    """
    for element in stock_data:
        stock_date=datetime.strptime(element['date'],'%Y-%m-%d').date()
        stmt = insert(StockData).values(
            ticker=ticker,
            stock_date=datetime.strptime(element['date'],'%Y-%m-%d').date(),
            Open=element["open"],
            high=element["high"],
            low=element["low"],
            close=element["close"],
            adjusted_close=element["adjusted_close"],
            volume=element["volume"],
            trade_day=trade_day
            )

        stmt = stmt.on_conflict_do_update(
            index_elements=['ticker','stock_date'],
            set_={
     #           'stock_date': stmt.excluded.stock_date,
                'Open': stmt.excluded.Open,
                "high": stmt.excluded.high,
                "low": stmt.excluded.low,
                "close": stmt.excluded.close,
                "adjusted_close": stmt.excluded.adjusted_close,
                "volume": stmt.excluded.volume,
            })
        db.execute(stmt)
    db.commit()

def update_values(db: Session, ticker: str, stock_date: date,values:dict):
    """Update Stock data by dict:
    example=volume={'volume':volume}"""
    stmt=(update(StockData).
          where(StockData.ticker==ticker).
          where(StockData.stock_date==stock_date).
          values(**values))
    result=db.execute(stmt)
    db.commit()

    if result.rowcount == 0:
        #do record to update
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(
            f"Update skipped: no row found for ticker={ticker}, stock_date={stock_date}"
        )
        return False
    else:
        return True
    
def insert_non_trading_days(
    db: Session,
    ticker: str,
    missing_dates: list[datetime]
):
    for d in missing_dates:
        stmt = insert(StockData).values(
            ticker=ticker,
            stock_date=d,
            trade_day=False,
            Open=0,
            high=0,
            low=0,
            close=0,
            adjusted_close=0,
            volume=0
        ).on_conflict_do_nothing(
            index_elements=["ticker", "stock_date"]
        )
        db.execute(stmt)
    db.commit()

    

def data_ticker_valid(db: Session, ticker: str, date_from: date, date_to: date):
    # check if DB contain all requested data with require dates.
    if type(date_from) ==date or  type(date_from) ==date :
        stmt = (
            select(StockData.stock_date)
            .where(StockData.ticker == ticker)
            .where(StockData.stock_date >= date_from)
            .where(StockData.stock_date <= date_to)
        )

        result = db.execute(stmt)
        rows= result.scalars().all()
        #scalars return all data in correct format

        # zamień na zbiór dat (stringi YYYY-MM-DD)
        existing = {datetime.strptime(row,'%Y-%m-%d').date() for row in rows}
        

        # sprawdź każdą datę w zakresie
        missing = []
        current = date_from
        while current <= date_to:
            if current != current.isoweekday() <5: #check only days 
                if current not in existing:
                    missing.append(current)
            current += timedelta(days=1)

        # zwróć True/False + listę brakujących dat
        return len(missing) == 0, missing
    else:
        logging.debug("Wrong datatype - date must be a date format")
        return False