from .db.crud import upsert_raw_data
from .db.database import get_session


session=get_session()
raw = ["testx"]
upsert_raw_data(session,"AAPL.US",raw)

