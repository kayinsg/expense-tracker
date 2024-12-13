from openpyxl import load_workbook
from openpyxl.styles import Alignment
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.worksheet import Worksheet as ExcelWorksheet

from pandas import DataFrame
from pandas import Series
import pendulum


from SupportInterfaces.FontFormatter import FontFormatter
from SupportInterfaces.TableConstructor import TableCreator
from SupportInterfaces.TypeChecker import TypeChecker
from SupportInterfaces.SummaryConstructor import RawSummary, Summary
from SupportInterfaces.dataTransferObjects import FontProfile, SpreadsheetDetails
from SupportInterfaces.utils import readLinesFromFile

import time
start_time = time.perf_counter()


class TableFacade:
    def __init__(self, flatTextPath: str):
        self.contentWithinFile = readLinesFromFile(flatTextPath)
        self.itemPricePairs = DataExtractor(
            self.contentWithinFile
        ).categorizeData()

    def getFlatTextFileList(self) -> list[str]:
        return self.contentWithinFile

    def getRawTable(self):
        return TableCreator(self.itemPricePairs).makeTable("raw")

    def getFormattedTable(self):
        return TableCreator(self.itemPricePairs).makeTable("view")


class DataExtractor:
    def __init__(self, listOfLinesInFile: list[str]):
        self.listOfLinesInFile = listOfLinesInFile

    def categorizeData(self) -> list[tuple[str, int | float | None]]:
        listOfLinesInFile = self.listOfLinesInFile

        items: list[str] = list(filter(
            self._lineComprisesStrings,
            listOfLinesInFile
        ))
        pricesRepresentedAsStrings: list[str] = list(filter(
            self._lineComprisesNumbers,
            listOfLinesInFile
        ))
        numericPrices: list[int | float | None] = list(map(
            self._convertPricesToNumericDataType,
            pricesRepresentedAsStrings
        ))
        afterTaxPrices = list(map(
            self._calculateAfterTaxPrices,
            numericPrices
        ))

        taxPaidPerItem = self._calculateTaxesPaidPerItem(
            numericPrices,
            afterTaxPrices
        )

        itemPriceInformation = list(zip(
            items,
            numericPrices,
            afterTaxPrices,
            taxPaidPerItem
        ))

        return itemPriceInformation

    def _lineComprisesStrings(self, entry) -> bool:
        entryType = TypeChecker(entry).dataType
        if entryType == "String":
            return True
        return False

    def _lineComprisesNumbers(self, entry) -> bool:
        entryType = TypeChecker(entry).dataType
        if entryType == "Integer":
            return True
        elif entryType == "Decimal":
            return True
        return False

    def _convertPricesToNumericDataType(self, price) -> int | float | None:
        dataTypeOfPrice = TypeChecker(price).dataType
        if dataTypeOfPrice == "Integer":
            return int(price)
        elif dataTypeOfPrice == "Decimal":
            return float(price)
        else:
            return None

    def _calculateAfterTaxPrices(self, price):
        countryTaxRateInDecimal = 0.13
        taxMultiplier = 1 + countryTaxRateInDecimal
        afterTaxPrice = taxMultiplier * price
        return afterTaxPrice

    def _calculateTaxesPaidPerItem(self, grossPrice, afterTaxPrice):
        pricePairs = list(zip(grossPrice, afterTaxPrice))

        taxesPaidPerItem = list()

        for grossPrice, afterTaxPrice in pricePairs:
            taxPaid = afterTaxPrice - grossPrice
            taxesPaidPerItem.append(taxPaid)

        return taxesPaidPerItem


class WorksheetCreator:
    def consolidateSpreadsheetDetails(self, filePath):
        workbook = self.getWorkbook(filePath)
        worksheet = self.createDateWorksheet(workbook)
        return SpreadsheetDetails(
            filePath,
            workbook,
            worksheet
        )

    def getWorkbook(self, filename):
        Workbook = load_workbook(
            filename, keep_vba=True, keep_links=True
        )
        return Workbook

    def createDateWorksheet(self, workbook) -> ExcelWorksheet:
        formattedCurrentDate = pendulum.now().format("MMM.DD.YYYY")
        worksheetName = f"{formattedCurrentDate} Budget"
        dateWorksheet = workbook.create_sheet(worksheetName, 0)
        return dateWorksheet


class SpreadsheetWriter:
    def __init__(
        self,
        spreadsheetDetails: SpreadsheetDetails,
        table: DataFrame,
        summary: Series
    ):
        self.spreadsheetDetails = spreadsheetDetails
        self.worksheet = spreadsheetDetails.worksheet
        self.table = table
        self.summary = summary

    def captureStateAfterWrite(self) -> SpreadsheetDetails:
        table = self.table
        summary = self.summary

        workbook = self.spreadsheetDetails.workbook
        spreadSheetFile = self.spreadsheetDetails.filePath

        self._writeTabularDataToWorksheet(table)
        self.writeSummaryToWorksheet(summary)

        workbook.save(spreadSheetFile)

        return SpreadsheetDetails(
            spreadSheetFile,
            workbook,
            self.spreadsheetDetails.worksheet
        )

    def _writeTabularDataToWorksheet(self, table) -> None:
        worksheet = self.spreadsheetDetails.worksheet
        workbook = self.spreadsheetDetails.workbook

        workbook.active = worksheet
        for row in dataframe_to_rows(
            table,
            index=False,
            header=True
        ):

            worksheet.append(row)

    def writeSummaryToWorksheet(self, series):
        summaryHeaders = list()
        summaryValues = list()

        indices = series.index.tolist()

        for index in indices:
            summaryHeaders.append(index)
            valueForSummary = series[index]
            summaryValues.append(valueForSummary)

        self.spreadsheetDetails.worksheet.append(summaryHeaders)
        self.spreadsheetDetails.worksheet.append(summaryValues)


class SpreadsheetColumnFormatter:
    def __init__(
        self,
        spreadsheetDetails : SpreadsheetDetails,
    ):

        self.spreadsheetDetails = spreadsheetDetails
        self.dataRows = self.spreadsheetDetails.worksheet.max_row

    def fetchFormattedWorkSheet(self):
        return self.formatColumns()

    def formatColumns(self):
        workbook = self.spreadsheetDetails.workbook
        filePath = self.spreadsheetDetails.filePath

        self.changeHeaderFont()
        self.changeBodyFont()
        self.adjustWidthOfColumnsToFit()
        self.padRowHeight()
        self.alignCellsBottomLeft()
        workbook.save(filePath)

        return SpreadsheetDetails(
            filePath,
            workbook,
            self.spreadsheetDetails.worksheet,
        )

    def changeHeaderFont(self):
        headerFontProfile = FontProfile(
            "Georgia",
            18,
            boldToggle = True
        )
        fontFormatter = FontFormatter(self.spreadsheetDetails)
        fontFormatter.changeHeaderFont(headerFontProfile)

    def changeBodyFont(self):
        bodyFontProfile = FontProfile(
            "Helvetica Neue",
            12.8,
            boldToggle = False
        )
        fontFormatter = FontFormatter(self.spreadsheetDetails)
        fontFormatter.changeBodyFont(bodyFontProfile)

    def adjustWidthOfColumnsToFit(self):
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

    def padRowHeight(self):
        worksheet = self.spreadsheetDetails.worksheet
        idealRowHeight = 27

        dataRows = worksheet.max_row + 1

        for row in range(1, dataRows):
            worksheet.row_dimensions[row].height = idealRowHeight

    def alignCellsBottomLeft(self):
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


flatTextFile = "/home/kayinfire/Documents/moreCompletedPurchaseList.txt"
spreadsheetFilePath = "/home/kayinfire/Downloads/inventory.xlsx"


def getTables():
    rawTable = TableFacade(flatTextFile).getRawTable()
    viewTable = TableFacade(flatTextFile).getFormattedTable()
    return {
        "Raw Table" : rawTable,
        "Formatted Table" : viewTable,
    }


def getSummaries():
    flatTextFileContent = TableFacade(flatTextFile).getFlatTextFileList()
    itemPricePairs = DataExtractor(flatTextFileContent).categorizeData()
    rawSummary = Summary(itemPricePairs).getRawSummary()
    formattedSummary = Summary(itemPricePairs).getFormattedSummary()
    return {
        "Raw Summary": rawSummary,
        "Formatted Summary" : formattedSummary,
    }


def createDateWorksheet():
    preparedSpreadsheet = WorksheetCreator().consolidateSpreadsheetDetails(
        spreadsheetFilePath
    )
    return preparedSpreadsheet


def writtenSpreadSheet(spreadsheetDetails):
    formattedTable = getTables()['Formatted Table']
    formattedSummary = getSummaries()['Formatted Summary']

    spreadsheetToBeWrittenTo = SpreadsheetWriter(
        spreadsheetDetails,
        formattedTable,
        formattedSummary

    )
    writtenSpreadSheet = spreadsheetToBeWrittenTo.captureStateAfterWrite()
    return writtenSpreadSheet


def formattedSpreadSheet(spreadsheetDetails):
    spreadsheetToBeFormatted = SpreadsheetColumnFormatter(spreadsheetDetails)
    formattedSpreadsheetDetails = spreadsheetToBeFormatted.fetchFormattedWorkSheet()
    return formattedSpreadsheetDetails.workbook.save(
        spreadsheetDetails.filePath
    )


end_time = time.perf_counter()
elapsed_time = end_time - start_time
