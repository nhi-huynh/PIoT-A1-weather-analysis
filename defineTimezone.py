import pytz 
from datetime import datetime, date, timedelta

DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT = "%H:%M:%S"
SHORT_TIME_FORMAT = "%H:%M"
ONE_DAY_DELTA = timedelta(days = 1)
ONE_HOUR_DELTA = timedelta(hours = 1)

timezone = pytz.timezone("Australia/Melbourne")
