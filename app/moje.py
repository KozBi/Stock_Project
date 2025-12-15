# from .db.crud import upsert_raw_data
# from .db.database import get_session
from datetime import datetime

# session=get_session()
# raw = ["testx"]
# upsert_raw_data(session,"AAPL.US",raw)


row='2023-01-03'
result=datetime.strptime(row,'%Y-%m-%d').date()
print(result)
print(type(result))