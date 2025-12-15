from datetime import datetime, timedelta

def any_missing_dates(days: list):
    """Check if any dates is missing in the middle of the list.\n
        Retrun missing dates or False"""
    dates = sorted(
        datetime.strptime(e["date"], "%Y-%m-%d").date()
        for e in days
    )

    start_date = dates[0]
    end_date = dates[-1]

    existing = set(dates)

    missing = []
    current = start_date
    while current <= end_date:
        if current not in existing:
            missing.append(current)
        current += timedelta(days=1)
    if missing == []:
        return False
    else: return missing
