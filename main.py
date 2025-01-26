from ExtractBudgetData.DataExtractor import DataFacade
from UpdateSpreadsheet.Spreadsheet import Spreadsheet
from paths import flatTextFile, spreadsheetPath

data = DataFacade(flatTextFile).formattedData()
Spreadsheet(spreadsheetPath).apply(data)
