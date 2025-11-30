import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, RawStockData, StockData
from app.db.crud import upsert_raw_data, upsert_stock_data

#Create temporary DB SQL lite for tests.
@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", echo=True)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


def test_upsert_raw_data(session):

    raw_data = {"price": 123.45, "volume": 1000}
    upsert_raw_data(session, "AAPL.US", raw_data)
    qrow=session.query(RawStockData).filter_by(ticker="AAPL.US").first()
    assert qrow.ticker =="AAPL.US"
    assert qrow.data["price"]==123.45
    assert qrow.data["volume"]==1000

    #instert a new record
    raw_data2 = {"price": 200.0, "volume": 500}
    upsert_raw_data(session, "test", raw_data2)
    row2 = session.query(RawStockData).filter_by(ticker="test").first()
    
    assert row2.ticker =="test"
    assert row2.data["price"] == 200.0
    assert row2.data["volume"] == 500

#[{'date': '2023-01-03', 'open': 130.28, 'high': 130.9, 'low': 124.17, 'close': 125.07, 'adjusted_close': 123.2112, 'volume': 112117500}, 

def test_upsert_stock_data(session,capsys):

    raw_data = [{'date': '2023-01-03', 'open': 130.28, 'high': 130.9, 'low': 124.17, 'close': 125.07, 'adjusted_close': 123.2112, 'volume': 112117500}]
    upsert_stock_data(session, "AAPL.US", raw_data)
    qrow=session.query(StockData).filter_by(ticker="AAPL.US").first()
    assert qrow.ticker =="AAPL.US"
    print(qrow.ticker)
   ## assert qrow.data["price"]==123.45
 ##   assert qrow.data["volume"]==1000
