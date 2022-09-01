#!/usr/bin/env python3

"""
Some simple notes on handling time in python.
See https://docs.python.org/3/library/datetime.html
"""

import datetime as dt
import time

# Timezones: datetime can handle timezones.
# It will probably use the platform's local timezone by default, and UTC should be set as the timezone if you really want it.
# datetime objects that have tzinfo=None are "naive" (vs "aware" if it has timezone info). The two can't be compared directly.

dt.datetime.now() # Current local date and time.
dt.datetime.now(dt.timezone.utc) # Current UTC date and time

# Daylight Saving Time:
# UTC doesn't do DST, but lots of other timezones do.
# In timezones with DST, timestamps can repeat (during the fall-back hour)
# In these cases, use datetime.fold to disambiguate between the earlier/later of the two moments.

# UNIX time:
# See the time module https://docs.python.org/3/library/time.html
# UNIX time - the number of seconds since the UNIX epoch (midnight on 1st Jan 1970 (UTC)), ignoring leap seconds
time.time() # Unix time (seconds), as a float
time.time_ns() # Unix time as an integer number of nanoseconds
time.time_ns() // 1000 # Unix time in milliseconds (no, there isn't a built-in for this)
dt.datetime.now().timestamp() # UNIX time, similar to time.time()

# UNIX time magnitude:
# https://en.wikipedia.org/wiki/Year_2038_problem
# The cut-off point for UNIX time on 32-bit systems is usually somewhere in 2038. (Since it's stored as a signed 32-bit int)
# The latest time is 2^31 - 1 (2,147,483,647) seconds after the epoch (03:14:07 UTC on 19 January 2038)
# *** So if the timestamp you're working with is larger than this number, it might be in milliseconds or nanoseconds instead! ***
dt.datetime.fromtimestamp(time.time()) # equiv. to dt.datetime.today() (no timezone info)

# ^ the fromtimestamp() method takes a UNIX timestamp in seconds (max 10 digits)!
# If working with ms (~16 digits) or ns (~19 digits), make sure to convert with //

# datetime objects:
# "A combination of a date and a time. Attributes: year, month, day, hour, minute, second, microsecond, and tzinfo."
# Comparisons (>, <, ==, etc.), adding timedelta, and subtracting another datetime to make a timedelta, are all possible.
t1 = dt.datetime.now() # A naive datetime object representing local date and time
t1.timestamp() # UNIX timestamp represented by this time
t1.month # The current month (1-12). Similar for year, day, etc.
t1.day # Day of the month (1-31)
t1.weekday() # Day of the week (0-6 meaning Mon-Sun). See also isoweekday() which gives 1-7.

# datetime formatting:
t1.isoformat() # YYYY-MM-DDTHH:MM:SS.ffffff (varies based on if microsecond is 0 and utcoffset)
t1.ctime() # e.g. "Fri Sep  2 00:17:52 2022"

# https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
# strftime formats a date, datetime or time object into a string.
# strptime parses a string into a datetime object.
# Both use the string-format spec in the above link
# Note: The format depends on the current locale, so be careful.
t1.strftime("%c") # %c - Locale’s appropriate date and time representation. (Seems the same as ctime)
t1.strftime("%d-%m-%Y") # DD-MM-YYYY format (note %y is 2-digit year)
t1.strftime("%H:%M:%S") # HH:MM:SS (%H - 24hr, %I - 12hr, %p - am/pm)
t1.strftime("%b - %B") # %b - Month as locale's abbreviated name (Jan-Dec), %B - Month as locale's full name (January-December)

t2 = dt.datetime.strptime("02-09-2022", "%d-%m-%Y") # Unspecified datetime attributes are taken from the default 1900-01-01T00:00:00.000

