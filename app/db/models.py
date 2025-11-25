from database import get_session
from sqlalchemy import Integer, String, Column, JSON
from sqlalchemy.orm import sessionmaker, declarative_base

Base= declarative_base()

class RawStockData(Base):
    __tablename__= "raw_stock_data"
    id = Column(Integer, primary_key=True)
    tcker = Column(String, nullable=False,unique=True)
    data=Column(JSON, nullable=False)

                

    

# from sqlalchemy import Column, Integer, String, Float, Date, JSON
# from database import Base  # importujemy Base z database.py

# class RawStockDatas(Base):
#     __tablename__ = "raw_stock_data"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     symbol = Column(String, nullable=False)
#     date = Column(Date, nullable=False)
#     raw = Column(JSON, nullable=False)  # cała odpowiedź API

# class StockData(Base):
#     __tablename__ = "stock_data"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     symbol = Column(String, nullable=False)
#     date = Column(Date, nullable=False)
#     open = Column(Float)
#     high = Column(Float)
#     low = Column(Float)
#     close = Column(Float)
#     volume = Column(Float)


