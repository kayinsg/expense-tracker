import pendulum
from typing import Callable, NamedTuple

class DateFormats(NamedTuple):
    iso: str
    spreadsheet: str

def getCurrentDate():
    dateFromPendulum = getDateFromPendulum
    return getCurrentDateObject(dateFromPendulum)

def getCurrentDateObject(dateProvider):
    dateStr = dateProvider()
    dateObj = pendulum.parse(dateStr)

    isoFormat = dateObj.format('YYYY-MM-DD')
    spreadsheetFormat = dateObj.format('MMM.DD.YYYY')

    return DateFormats(iso=isoFormat, spreadsheet=spreadsheetFormat)

def getDateFromPendulum():
    return pendulum.now().to_date_string()
