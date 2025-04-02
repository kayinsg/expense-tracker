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


class HeaderFormatter(FontFormatterInterface):
    def __init__(
        self,
        worksheet,
        headerRowNumbers
    ):
        self.worksheet = worksheet
        self.headerRowNumbers = headerRowNumbers

    def changeFont(self, FontProfile) -> None:
        worksheet = self.worksheet
        lastColumnContainingData = worksheet.max_column + 1
        for headerRow in self.headerRowNumbers:
            for columnNumber in range(1, lastColumnContainingData):

                headerCell = worksheet.cell(row=headerRow, column=columnNumber)
                headerCell.font = Font(
                    name=FontProfile.name,
                    size=FontProfile.size,
                    bold=FontProfile.boldToggle
                )


class BodyFormatter(FontFormatterInterface):
    def __init__(self, worksheet, bodyRowNumbers):
        self.worksheet = worksheet
        self.bodyRowNumbers = bodyRowNumbers

    def changeFont(self, FontProfile) -> None:
        worksheet = self.worksheet
        lastColumnContainingData = worksheet.max_column + 1
        for bodyRow in self.bodyRowNumbers:
            for columnNumber in range(
                1,
                lastColumnContainingData
            ):
                headerCell = worksheet.cell(
                    row=bodyRow,
                    column=columnNumber
                )
                headerCell.font = Font(
                    name=FontProfile.name,
                    size=FontProfile.size,
                    bold=FontProfile.boldToggle
                )


class TypeOfRowIdentifier:
    def __init__(self, worksheet):
        self.rows = self.getSheetData(worksheet)

    @staticmethod
    def getSheetData(worksheet):
        data = []
        for row in worksheet.iter_rows(values_only=True):
            data.append(list(row))
        return data

    def fetchRowNumbers(self, rowType):
        if rowType == "headers":
            return self.getHeaderRowNumbers()
        elif rowType == "body":
            return self.getBodyRowNumbers() 

    def getHeaderRowNumbers(self):
        headerRowNumbers = [ ]
        for index, row in enumerate(self.rows, start=1):
            if self.typeOfRow(row) == "Header":
                headerRowNumbers.append(index)
        return headerRowNumbers

    def getBodyRowNumbers(self):
        bodyRowNumbers = [ ]
        for index, row in enumerate(self.rows, start=1):
            if self.typeOfRow(row) == "Body":
                bodyRowNumbers.append(index)
        return bodyRowNumbers

    def typeOfRow(self, row):
        for item in row:
            if '$' in str(item):
                return 'Body'
        return 'Header'
