import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, RawStockData
from app.db.crud import upsert_raw_data

#Create temporary DB SQL lite for tests.
@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


def test_upsert(session,capsys):

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
