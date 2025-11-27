from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# -----------------------------------------
# Load Variables form .env
# -----------------------------------------
load_dotenv()


# -----------------------------------------
# Database URL
# -----------------------------------------
# Format: dialect+driver://username:password@host:port/database

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "stock_db")

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# -----------------------------------------
# Create engie
# -----------------------------------------
engine = create_engine(DATABASE_URL, echo=True) 
Base=declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    return SessionLocal()

