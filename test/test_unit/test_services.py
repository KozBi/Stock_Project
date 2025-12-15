from app.services.stock_calendar import any_missing_dates
import datetime
import pytest

days=[{'date': '2023-01-03', 'open': 130.28, 'high': 130.9, 'low': 124.17, 'close': 125.07, 'adjusted_close': 123.2112, 'volume': 112117500}, 
                {'date': '2023-01-04', 'open': 126.89, 'high': 128.66, 'low': 125.08, 'close': 126.36, 'adjusted_close': 124.482, 'volume': 89113600},
                {'date': '2023-01-05', 'open': 127.13, 'high': 127.77, 'low': 124.76, 'close': 125.02, 'adjusted_close': 123.162, 'volume': 80962700},
                {'date': '2023-01-09', 'open': 130.47, 'high': 133.41, 'low': 129.89, 'close': 130.15, 'adjusted_close': 128.2157, 'volume': 70790800}, 
                {'date': '2023-01-10', 'open': 130.26, 'high': 131.26, 'low': 128.12, 'close': 130.73, 'adjusted_close': 128.7871, 'volume': 63896200},
                {'date': '2023-01-12', 'open': 133.88, 'high': 134.26, 'low': 131.44, 'close': 133.41, 'adjusted_close': 131.4273, 'volume': 71379600}, 
                {'date': '2023-01-13', 'open': 132.03, 'high': 134.92, 'low': 131.66, 'close': 134.76, 'adjusted_close': 132.7572, 'volume': 57809700}] 

def test_any_missing_dates():
    result=any_missing_dates(days)
    assert len(result)==4
    assert (datetime.date(2023, 1, 6) in result)
    assert (datetime.date(2023, 1, 7) in result)
    assert (datetime.date(2023, 1, 8) in result)
    assert (datetime.date(2023, 1, 11) in result)
