from UpdateSpreadsheet.WorksheetFormatter import SpreadsheetFormatter
from paths import flatTextFile, saveDirectoryForSpreadsheets
import pendulum

from UpdateSpreadsheet.FileSystem import FileSystem
from UpdateSpreadsheet.WorkbookPopulator import WorkbookPopulator
from UpdateSpreadsheet.WorksheetWriter import WorksheetDataDepositor
from UpdateSpreadsheet.utils import DateTranslator

class Spreadsheet:
    def execute(self):
        currentDate = self.getCurrentdate()
        workbook = FileSystem(saveDirectoryForSpreadsheets).setUpSpreadsheet(currentDate)
        workbookWithDateWorksheets = WorkbookPopulator(currentDate).populate(workbook['Workbook'])
        currentSpreadsheetDate = self.getCurrentdate()

        worksheet = self.insertDataInSpreadsheet(workbookWithDateWorksheets, currentSpreadsheetDate, dataFromTextFile)
        SpreadsheetFormatter(worksheet).apply()
        workbook['Workbook'].save(workbook['FilePath'])

    def getCurrentdate(self):
        date = pendulum.now().format('YYYY-MM-DD')
        return DateTranslator(date).convert()

    def insertDataInSpreadsheet(self, workbookWithDateWorksheets, spreadsheetDate):
        workbookFilledWithData = WorksheetDataDepositor(workbookWithDateWorksheets, spreadsheetDate).insert(budgetInfo)
        return workbookFilledWithData[spreadsheetDate]

Spreadsheet().execute()
