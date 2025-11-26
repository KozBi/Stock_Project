from sqlalchemy.orm import Session
from .models import RawStockData
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
