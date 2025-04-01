from abc import abstractmethod
from openpyxl import load_workbook
import openpyxl
from openpyxl.styles import Alignment
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.worksheet import Worksheet as ExcelWorksheet

from pandas import DataFrame
from pandas import Series
import pendulum


from UpdateSpreadsheet.FontFormatter import FontFormatter
from paths import spreadsheetPath
from abc import abstractmethod, ABC
from UpdateSpreadsheet.dataObjects import SpreadsheetDetails, FontProfile
from GlobalDataObjects import Data
from UpdateSpreadsheet.dataTypes import ExcelWorkbook, ExcelWorksheet


class Spreadsheet:
    def __init__(self, filePath: str):
        self.filePath = filePath

    def apply(self):
        formattedWorksheet = SpreadsheetFormatter(writtenWorksheet).apply()
        formattedWorksheet.workbook.save(self.filePath)
        return formattedWorksheet


class SpreadsheetInterface(ABC):
    @abstractmethod
    def apply(self) -> SpreadsheetDetails:
        raise NotImplementedError(
            'This is an abstract class.'
            'Desist from trying to instantiate'
        )


class SpreadsheetFormatter(SpreadsheetInterface):
    def __init__(
        self,
        spreadsheetDetails : SpreadsheetDetails,
    ):

        self.spreadsheetDetails = spreadsheetDetails
        self.dataRows = self.spreadsheetDetails.worksheet.max_row

    def apply(self) -> SpreadsheetDetails:
        workbook = self.spreadsheetDetails.workbook
        filePath = self.spreadsheetDetails.filePath

        self.changeHeaderFont()
        self.changeBodyFont()
        self.adjustWidthOfColumnsToFit()
        self.padRowHeight()
        self.alignCellsBottomLeft()

        return SpreadsheetDetails(
            filePath,
            workbook,
            self.spreadsheetDetails.worksheet,
        )

    def changeHeaderFont(self) -> None:
        headerFontProfile = FontProfile(
            "Georgia",
            18,
            boldToggle = True
        )
        fontFormatter = FontFormatter(self.spreadsheetDetails)
        fontFormatter.changeHeaderFont(headerFontProfile)

    def changeBodyFont(self) -> None:
        bodyFontProfile = FontProfile(
            "Helvetica Neue",
            12.8,
            boldToggle = False
        )
        fontFormatter = FontFormatter(self.spreadsheetDetails)
        fontFormatter.changeBodyFont(bodyFontProfile)

    def adjustWidthOfColumnsToFit(self) -> None:
        worksheet = self.spreadsheetDetails.worksheet

        for column in worksheet.iter_cols():
            currentColumnIndex = ""
            maxLengthOfCellInColumn = 0

            for cell in column:
                currentColumnIndex = cell.column_letter
                lengthOfCellValue = len(str(cell.value))
                if lengthOfCellValue > maxLengthOfCellInColumn:
                    maxLengthOfCellInColumn = lengthOfCellValue

            worksheet.column_dimensions[currentColumnIndex].width = maxLengthOfCellInColumn + 8

    def padRowHeight(self) -> None:
        worksheet = self.spreadsheetDetails.worksheet
        idealRowHeight = 27

        dataRows = worksheet.max_row + 1

        for row in range(1, dataRows):
            worksheet.row_dimensions[row].height = idealRowHeight

    def alignCellsBottomLeft(self) -> None:
        worksheet = self.spreadsheetDetails.worksheet
        lastDataColumnAccountedForRange = worksheet.max_column

        for row in worksheet.iter_rows(
                max_row=self.dataRows,
                max_col=lastDataColumnAccountedForRange
        ):
            for cell in row:
                cell.alignment = Alignment(
                    horizontal="left",
                    vertical="bottom"
                )
