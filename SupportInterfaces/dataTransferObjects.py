from typing import NamedTuple
from dataclasses import dataclass

from openpyxl import Workbook as ExcelWorkbook
from openpyxl.worksheet.worksheet import Worksheet as ExcelWorksheet
from pandas import DataFrame, Series


class ColumnDetails(NamedTuple):
    name: str
    values: list


class SpreadsheetDetails(NamedTuple):
    filePath            : str
    workbook            : ExcelWorkbook
    worksheet           : ExcelWorksheet


class FontProfile(NamedTuple):
    name       : str
    size       : int | float
    boldToggle : bool


@dataclass
class RowInfo:
    headerRowNumbers : list[int]
    bodyRowNumbers   : list[int]

class Data(NamedTuple):
    table: DataFrame
    summary: Series



NonIterable = str | float | int
AtomicDataStructure    = str | float | int
CompositeDataStructure =  list | tuple | set
