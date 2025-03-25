from pandas import DataFrame
import openpyxl

class SpreadsheetDataPopulator:
    def __init__(self, currentDate: str, dataFrame: DataFrame):
        self.currentDate = currentDate
        self.dataFrame = dataFrame

    def populate(self, workbook: openpyxl.Workbook) -> openpyxl.Workbook:
        dateWorksheet = self.getWorksheetForCurrentDate(workbook)
        dataList = self.convertDataFrameToList(self.dataFrame)
        self.writeDataToTheCurrentDateWorksheet(dataList, dateWorksheet)
        return workbook

    def getWorksheetForCurrentDate(self, workbook):
        return workbook[self.currentDate]

    def convertDataFrameToList(self, dataFrame):
        return [dataFrame.columns.tolist()] + dataFrame.values.tolist()

    def writeDataToTheCurrentDateWorksheet(self, dataList, worksheet):
        for row_num, row_data in enumerate(dataList, start=1):
            self.writeRowToWorksheet(worksheet, row_num, row_data)

    def writeRowToWorksheet(self, worksheet, row_num, row_data):
        for col_num, cell_value in enumerate(row_data, start=1):
            worksheet.cell(row=row_num, column=col_num, value=cell_value)
