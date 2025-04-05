from ExtractBudgetData.DataExtractor import DataFacade
from UpdateSpreadsheet.SpreadsheetFormatter import SpreadsheetFormatter
from paths import flatTextFile, saveDirectoryForSpreadsheets
import pendulum

from UpdateSpreadsheet.FileSystem import FileSystem
from UpdateSpreadsheet.WorkbookPopulator import WorkbookPopulator
from UpdateSpreadsheet.SpreadsheetWriter import WorksheetDataDepositor
from UpdateSpreadsheet.utils import DateTranslator

class Spreadsheet:
    def execute(self):
        currentIsoDate = self.getCurrentdate('iso')
        workbook = self.createCreateSpreadsheetOnFileSystem(currentIsoDate)
        workbookWithDateWorksheets = self.populateWorkbookWithWorksheets(workbook, currentIsoDate)
        currentSpreadsheetDate = self.getCurrentdate('spreadsheet')
        dataFromTextFile = self.extractDataFromTextFile()
        worksheet = self.insertDataInSpreadsheet(workbookWithDateWorksheets, currentSpreadsheetDate, dataFromTextFile)
        SpreadsheetFormatter(worksheet).apply()
        workbook['Workbook'].save(workbook['FilePath'])

    def getCurrentdate(self, typeOfDate):
        date = pendulum.now().format('YYYY-MM-DD')
        return DateTranslator(date).translateDate(typeOfDate)

    def extractDataFromTextFile(self):
        return DataFacade(flatTextFile).get("Formatted")

    def createCreateSpreadsheetOnFileSystem(self, date):
        return FileSystem(saveDirectoryForSpreadsheets).setUpSpreadsheet(date)

    def populateWorkbookWithWorksheets(self, workbook, currentDate):
        return WorkbookPopulator(currentDate).populate(workbook['Workbook']) 

    def insertDataInSpreadsheet(self, workbookWithDateWorksheets, spreadsheetDate, data):
        workbookFilledWithData = WorksheetDataDepositor(workbookWithDateWorksheets, spreadsheetDate).insert(data.table, data.summary)
        return workbookFilledWithData[spreadsheetDate]

Spreadsheet().execute()
