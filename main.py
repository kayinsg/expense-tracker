from ExtractBudgetData.DataExtractor import DataFacade
from UpdateSpreadsheet.Spreadsheet import Spreadsheet
from paths import flatTextFile, spreadsheetPath

data = DataFacade(flatTextFile).get("Formatted")
Spreadsheet(spreadsheetPath).apply(data)
