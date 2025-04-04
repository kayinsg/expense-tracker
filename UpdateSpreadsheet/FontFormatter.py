from abc import ABC, abstractmethod
import re as regex

from openpyxl.styles import Font
from collections import defaultdict


class FontFormatter:
    def __init__(self, spreadsheetDetails):
        self.worksheet = spreadsheetDetails.worksheet
        self.workbook = spreadsheetDetails.workbook

    def changeHeaderFont(self, FontProfile) -> None:
        headerRowNumbers = self.getRowNumbers('header')
        HeaderFormatter(self.worksheet, headerRowNumbers).changeFont(FontProfile)

    def changeBodyFont(self, FontProfile) -> None:
        headerRowNumbers = self.getRowNumbers('body')
        BodyFormatter(self.worksheet, headerRowNumbers).changeFont(FontProfile)

    def getRowNumbers(self, rowType):
        return TypeOfRowIdentifier(self.worksheet).fetchRowNumbers(rowType)


class FontFormatterInterface(ABC):
    @abstractmethod
    def changeFont(self, FontProfile) -> None:
        raise NotImplementedError(
            'This is an abstract class.'
            'Desist from trying to instantiate'
        )

    def getColumnNumbersThatContainData(self, worksheet):
        lastNonEmptyColumnAccountedForRange = worksheet.lastColumnContainingData + 1
        columnNumbers = [ ]
        for columnNumber in range(1, lastNonEmptyColumnAccountedForRange):
            columnNumbers.append(columnNumber)
        return columnNumbers


class HeaderFormatter(FontFormatterInterface):
    def __init__(
        self,
        worksheet,
        headerRowNumbers
    ):
        self.worksheet = worksheet
        self.headerRowNumbers = headerRowNumbers
        self.lastColumnContainingData = worksheet.max_column + 1

    def changeFont(self, FontProfile) -> None:
        for headerRow in self.headerRowNumbers:
            for columnNumber in self.getColumnNumbersThatContainData(self.worksheet):
                cellCoordinates = {'rowNumber':headerRow, 'columnNumber': columnNumber}
                self.changeHeaderRows(FontProfile, cellCoordinates)

    def changeHeaderRows(self, FontProfile, cellCoordinates):
        cellObject = self.getCellObject(cellCoordinates) 
        self.changeCellFontProperties(FontProfile, cellObject)

    def getCellObject(self, cellCoordinates):
        headerCell = self.worksheet.cell(
            row=cellCoordinates['rowNumber'],
            column=cellCoordinates['columnNumber']
        )
        return headerCell

    def changeCellFontProperties(self, FontProfile, headerCell):
        headerCell.font = Font(
            name=FontProfile.name,
            size=FontProfile.size,
            bold=FontProfile.boldToggle
        )


class BodyFormatter(FontFormatterInterface):
    def __init__(self, worksheet, bodyRowNumbers):
        self.worksheet = worksheet
        self.bodyRowNumbers = bodyRowNumbers
        self.lastColumnContainingData = worksheet.max_column + 1

    def changeFont(self, FontProfile) -> None:
        for bodyRow in self.bodyRowNumbers:
            for columnNumber in self.getColumnNumbersThatContainData(self.worksheet):
                cellCoordinates = {'rowNumber':bodyRow, 'columnNumber': columnNumber}
                self.changeBodyRows(FontProfile, cellCoordinates)

    def changeBodyRows(self, FontProfile, cellCoordinates):
        cellObject = self.getCellObject(cellCoordinates)
        self.changeCellFontProperties(FontProfile, cellObject)

    def getCellObject(self, cellCoordinates):
        bodyCell = self.worksheet.cell(
            row=cellCoordinates['rowNumber'],
            column=cellCoordinates['columnNumber']
        )
        return bodyCell

    def changeCellFontProperties(self, FontProfile, bodyCell):
        bodyCell.font = Font(
            name=FontProfile.name,
            size=FontProfile.size,
            bold=FontProfile.boldToggle
        )


class TypeOfRowIdentifier:
    def __init__(self, worksheet):
        self.worksheet = worksheet

    def fetchRowNumbers(self, rowType):
        worksheetData = self.getSheetData(self.worksheet)
        if rowType == "headers":
            return self.getHeaderRowNumbers(worksheetData)
        elif rowType == "body":
            return self.getBodyRowNumbers(worksheetData)

    def getSheetData(self, worksheet):
        data = []
        for row in worksheet.iter_rows(values_only=True):
            data.append(list(row))
        return data

    def getHeaderRowNumbers(self, worksheetDataRows):
        headerRowNumbers = [ ]
        for index, row in enumerate(worksheetDataRows, start=1):
            if self.typeOfRow(row) == "Header":
                headerRowNumbers.append(index)
        return headerRowNumbers

    def getBodyRowNumbers(self, worksheetDataRows):
        bodyRowNumbers = [ ]
        for index, row in enumerate(worksheetDataRows, start=1):
            if self.typeOfRow(row) == "Body":
                bodyRowNumbers.append(index)
        return bodyRowNumbers

    def typeOfRow(self, row):
        for item in row:
            if '$' in str(item):
                return 'Body'
        return 'Header'
