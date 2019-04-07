import pytz
from datetime import datetime, date, timedelta

timezone = pytz.timezone("Australia/Melbourne")

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
ONE_DAY_DELTA = timedelta(days=1)
ONE_HOUR_DELTA = timedelta(hours=1)
