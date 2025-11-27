from .database import get_session, engine
from sqlalchemy import Integer, String, Column, JSON , Date , UniqueConstraint
from sqlalchemy.orm import sessionmaker, declarative_base

Base= declarative_base()

class RawStockData(Base):
    __tablename__= "raw_stock_data"
    id = Column(Integer, primary_key=True)
    ticker = Column(String, nullable=False,unique=True)
    date= Column(Date, nullable=False)
    data=Column(JSON, nullable=False) 



Base.metadata.create_all(engine)