from .database import get_session, engine
from sqlalchemy import Integer, String, Column, JSON , Date , UniqueConstraint , Float , Index
from sqlalchemy.orm import sessionmaker, declarative_base

Base= declarative_base()

class RawStockData(Base):
    __tablename__= "raw_stock_data"
    id = Column(Integer, primary_key=True)
    ticker = Column(String, nullable=False,unique=True)
    date= Column(Date, nullable=False)
    data=Column(JSON, nullable=False) 

class StockData(Base):
    __tablename__= "stock_data"
    id = Column(Integer, primary_key=True,)
    ticker = Column(String, nullable=False)
    stock_date= Column(String, nullable=False)
    Open=Column(Float, nullable=False) 
    high=Column(Float, nullable=False) 
    low=Column(Float, nullable=False) 
    close=Column(Float, nullable=False) 
    adjusted_close=Column(Float, nullable=False) 
    volume=Column(Integer, nullable=False) 

    
    __table_args__ = (
        # Prevent duplicate daily records for the same ticker
        UniqueConstraint("ticker", "stock_date", name="uix_ticker_date"),
        
        # Speed up SELECT queries filtering by ticker (e.g., get all AAPL rows)
        Index("idx_ticker", "ticker"),
    )

Base.metadata.create_all(engine)