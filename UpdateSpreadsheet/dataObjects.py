from pandas import DataFrame, Series
from typing import NamedTuple
import openpyxl

class SpreadsheetDetails(NamedTuple):
    filePath            : str
    workbook            : openpyxl.workbook.workbook.Workbook
    worksheet           : openpyxl.worksheet.worksheet.Worksheet

class FontProfile(NamedTuple):
    name       : str
    size       : int | float
    boldToggle : bool
