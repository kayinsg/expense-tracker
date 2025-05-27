from ExtractBudgetData.Cost import Cost
from ExtractBudgetData.TextFile import TextFile

from UpdateSpreadsheet.DateTranslator import getCurrentDate
from UpdateSpreadsheet.FileSystem import FileSystem
from UpdateSpreadsheet.WorkbookPopulator import WorkbookPopulator
from UpdateSpreadsheet.WorksheetFormatter import SpreadsheetFormatter
from UpdateSpreadsheet.WorksheetWriter import WorksheetDataDepositor

from paths import flatTextFile, saveDirectoryForSpreadsheets

def createSpreadsheet():
    textFileData = TextFile(flatTextFile).extractData()
    budgetInfo = Cost(textFileData).getBudgetInfo('formatted')
    currentDate = getCurrentDate()
    workbook = FileSystem(saveDirectoryForSpreadsheets).setUpSpreadsheet(currentDate.iso)
    workbookWithDateWorksheets = WorkbookPopulator(currentDate.iso).populate(workbook['Workbook'])
    worksheet = WorksheetDataDepositor(workbookWithDateWorksheets, currentDate.spreadsheet).insert(budgetInfo)
    SpreadsheetFormatter(worksheet[currentDate.spreadsheet]).apply()
    workbook['Workbook'].save(workbook['FilePath'])

createSpreadsheet()
