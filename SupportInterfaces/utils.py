from .TypeChecker import TypeChecker
from pandas import DataFrame
from .dataTransferObjects import ColumnDetails


def getDollarColumns(table: DataFrame):
    totalColumnsObject = table.columns
    totalColumns: list[str] = totalColumnsObject.tolist()
    dollarColumns = list()
    for column in totalColumns:
        columnValues = table[column].tolist()
        if TypeChecker(columnValues).dataType == "Decimal":
            dollarColumns.append(ColumnDetails(column, columnValues))
        else:
            pass
    return dollarColumns


def readLinesFromFile(filePath):
    with open(filePath, "r") as file:
        return file.read().splitlines()
