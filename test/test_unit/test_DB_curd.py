import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, RawStockData, StockData
from app.db.crud import upsert_raw_data, upsert_stock_data, update_values

#Create temporary DB SQL lite for tests.
@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", echo=True)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    yield db
    db.close()

@pytest.fixture
def session_with_values():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    more_values=[{'date': '2023-01-03', 'open': 130.28, 'high': 130.9, 'low': 124.17, 'close': 125.07, 'adjusted_close': 123.2112, 'volume': 112117500}, 
                {'date': '2023-01-04', 'open': 126.89, 'high': 128.66, 'low': 125.08, 'close': 126.36, 'adjusted_close': 124.482, 'volume': 89113600},
                {'date': '2023-01-05', 'open': 127.13, 'high': 127.77, 'low': 124.76, 'close': 125.02, 'adjusted_close': 123.162, 'volume': 80962700},
                {'date': '2023-01-09', 'open': 130.47, 'high': 133.41, 'low': 129.89, 'close': 130.15, 'adjusted_close': 128.2157, 'volume': 70790800}, 
                {'date': '2023-01-10', 'open': 130.26, 'high': 131.26, 'low': 128.12, 'close': 130.73, 'adjusted_close': 128.7871, 'volume': 63896200},
                {'date': '2023-01-12', 'open': 133.88, 'high': 134.26, 'low': 131.44, 'close': 133.41, 'adjusted_close': 131.4273, 'volume': 71379600}, 
                {'date': '2023-01-13', 'open': 132.03, 'high': 134.92, 'low': 131.66, 'close': 134.76, 'adjusted_close': 132.7572, 'volume': 57809700}] 
    
    upsert_stock_data(db, "AAPL.US", more_values)
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

def test_upsert_stock_data(session,capsys):

    raw_data = [{'date': '2023-01-03', 'open': 130.28, 'high': 130.9, 'low': 124.17, 'close': 125.07, 'adjusted_close': 123.2112, 'volume': 112117500}]
    upsert_stock_data(session, "AAPL.US", raw_data)
    qrow=session.query(StockData).filter_by(ticker="AAPL.US").first()
    assert qrow.ticker =="AAPL.US"
    assert qrow.volume ==112117500
    assert qrow.high == 130.9
    
    raw_data = [{'date': '2023-01-03', 'open': 130.28, 'high': 130.9, 'low': 124.17, 'close': 125.07, 'adjusted_close': 123.2112, 'volume': 200}]
    upsert_stock_data(session, "AAPL.US", raw_data)
    qrow=session.query(StockData).filter_by(ticker="AAPL.US").first()
    assert qrow.volume ==200

def test_upsert_more_values(session,capsys):

    more_values=[{'date': '2023-01-03', 'open': 130.28, 'high': 130.9, 'low': 124.17, 'close': 125.07, 'adjusted_close': 123.2112, 'volume': 112117500}, 
                {'date': '2023-01-04', 'open': 126.89, 'high': 128.66, 'low': 125.08, 'close': 126.36, 'adjusted_close': 124.482, 'volume': 89113600},
                {'date': '2023-01-05', 'open': 127.13, 'high': 127.77, 'low': 124.76, 'close': 125.02, 'adjusted_close': 123.162, 'volume': 80962700},
                {'date': '2023-01-09', 'open': 130.47, 'high': 133.41, 'low': 129.89, 'close': 130.15, 'adjusted_close': 128.2157, 'volume': 70790800}, 
                {'date': '2023-01-10', 'open': 130.26, 'high': 131.26, 'low': 128.12, 'close': 130.73, 'adjusted_close': 128.7871, 'volume': 63896200},
                {'date': '2023-01-12', 'open': 133.88, 'high': 134.26, 'low': 131.44, 'close': 133.41, 'adjusted_close': 131.4273, 'volume': 71379600}, 
                {'date': '2023-01-13', 'open': 132.03, 'high': 134.92, 'low': 131.66, 'close': 134.76, 'adjusted_close': 132.7572, 'volume': 57809700}]
    upsert_stock_data(session, "AAPL.US", more_values)
    qrows=session.query(StockData).filter_by(ticker="AAPL.US").all()
    assert type(qrows)==list
    assert type(qrows[0])==StockData
    assert len(qrows)==7
    assert (qrows[6].volume)==57809700

def test_update_values(session_with_values,capsys):
    _ticker="AAPL.US"

    update_values(session_with_values,_ticker,'2023-01-03',{'volume':100})
    row=session_with_values.query(StockData).filter_by(stock_date='2023-01-03').all()
    assert (row[0].volume)==100

    date_list=[['2023-01-04',{'volume':100}],['2023-01-05',{'Open':100}],['2023-01-09',{'close':100,'volume':50}]]

    for d in date_list:
         update_values(session_with_values,_ticker,d[0],d[1])

    row_1=session_with_values.query(StockData).filter_by(stock_date='2023-01-04').first()
    row_2=session_with_values.query(StockData).filter_by(stock_date='2023-01-05').first()
    row_3=session_with_values.query(StockData).filter_by(stock_date='2023-01-09').first()
    row_4=session_with_values.query(StockData).filter_by(stock_date='2023-01-06').first()

    assert (row_1.volume)==100
    assert (row_2.Open)==100
    assert (row_3.close)==100
    assert (row_3.volume)==50

         

        # with capsys.disabled():
        #         print(d[0])
        #         print(d[1])





# d