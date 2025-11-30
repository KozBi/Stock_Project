from sqlalchemy.orm import Session
from .models import RawStockData, StockData
from datetime import date
from sqlalchemy.dialects.postgresql import insert

def upsert_raw_data(db: Session, ticker: str, raw_json: dict):
    """
    Save one raw stock data entry into the database.
    """
    init_date=date.today()

    stmt = insert(RawStockData).values(
        ticker=ticker,
        date=init_date,
        data=raw_json
        )

    stmt = stmt.on_conflict_do_update(
        index_elements=['ticker'],
        set_=dict(data=raw_json)
    )
    db.execute(stmt)
    db.commit()

def upsert_stock_data(db: Session, ticker: str, stock_data: list):
    """
    Save data from row_data - Transfer Data
    """
    for element in stock_data:

        a=element["date"],

        stmt = insert(StockData).values(
            ticker=ticker,
            stock_date=element['date'],
            Open=element["open"],
            high=element["high"],
            low=element["low"],
            close=element["close"],
            adjusted_close=element["adjusted_close"],
            volume=element["volume"],
            )

        stmt = stmt.on_conflict_do_update(
            index_elements=['ticker','date'],
            set_={
                'stock_date': stmt.excluded.stock_date,
                "high": stmt.excluded.high,
                "low": stmt.excluded.low,
                "close": stmt.excluded.close,
                "adjusted_close": stmt.excluded.adjusted_close,
                "volume": stmt.excluded.volume,
            })
        db.execute(stmt)
    db.commit()